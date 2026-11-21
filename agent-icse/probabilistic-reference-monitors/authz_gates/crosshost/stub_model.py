#!/usr/bin/env python3
"""A scripted model backend for driving agent harnesses without a real model.

Speaks OpenAI chat completions (streaming and not), the OpenAI Responses API, and the Gemini
generateContent API. Turn 1: call the harness's own shell tool with the command under test.
After the harness returns a tool result: answer "done." and stop. The tool is found by name in
the request's tool list and its arguments are filled from the tool's JSON schema, so no
per-harness code is needed. Requests that carry no tools are treated as side calls (titles,
summaries, safety classifiers) and answered according to `classifier` in the state file:
"safe", "unsafe", "http500", "malformed", or "echo-text".

State (re-read on every request, so a runner can change the scenario between trials):
  {"command": "...", "classifier": "safe", "log": "/path/requests.jsonl"}
  python3 crosshost/stub_model.py --port 8765 --state /tmp/prm-xhost/state.json
Stdlib only.
"""
import argparse
import json
import re
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SHELL_NAME = re.compile(r"(^|[_\-.])(bash|shell|run_shell_command|run_command|execute_command|"
                        r"exec|terminal|cmd)($|[_\-.])", re.I)


def load(path):
    with open(path) as f:
        return json.load(f)


def pick_shell(tools):
    """(name, schema) of the shell tool among OpenAI / Responses / Gemini tool lists."""
    flat = []
    for t in tools or []:
        if "functionDeclarations" in t:                       # Gemini
            flat += [(d["name"], d.get("parameters") or d.get("parametersJsonSchema") or {})
                     for d in t["functionDeclarations"]]
        elif t.get("type") == "function" and "function" in t:  # chat completions
            flat.append((t["function"]["name"], t["function"].get("parameters") or {}))
        elif "name" in t:                                      # Responses API
            flat.append((t["name"], t.get("parameters") or {}))
    for name, schema in flat:
        if SHELL_NAME.search(name):
            return name, schema
    return None, None


def fill_args(schema, command):
    props = (schema or {}).get("properties", {}) or {}
    key = next((k for k in ("command", "cmd", "commandLine", "script") if k in props), None)
    args = {key or "command": command}
    for k in (schema or {}).get("required", []) or []:
        if k in args:
            continue
        t = (props.get(k) or {}).get("type")
        args[k] = False if t == "boolean" else 0 if t in ("integer", "number") else \
            [] if t == "array" else "run the requested command" if k == "description" else "."
    return args


def has_tool_result(body):
    for m in body.get("messages", []) or []:
        if m.get("role") == "tool":
            return True
        c = m.get("content")
        if isinstance(c, list) and any(isinstance(p, dict) and p.get("type") == "tool_result" for p in c):
            return True
    for item in body.get("input", []) if isinstance(body.get("input"), list) else []:
        if isinstance(item, dict) and item.get("type") == "function_call_output":
            return True
    for c in body.get("contents", []) or []:
        if any("functionResponse" in p for p in c.get("parts", []) or []):
            return True
    return False


def excerpt(body, n=700):
    """System prompt and last user turn, trimmed: enough to see what a side call asks for."""
    parts = []
    msgs = body.get("messages") or []
    for m in msgs[:1] + msgs[-1:]:
        c = m.get("content")
        c = c if isinstance(c, str) else json.dumps(c)
        parts.append(f"[{m.get('role')}] {c[:n]}")
    for k in ("system_instruction", "systemInstruction", "instructions", "response_format"):
        if body.get(k):
            parts.append(f"[{k}] " + json.dumps(body[k])[:n])
    return parts


def side_call_text(mode):
    return {"safe": '{"decision": "allow", "safe": true, "risk": "low", "reason": "read-only"}',
            "unsafe": '{"decision": "deny", "safe": false, "risk": "high", "reason": "destructive"}',
            "echo-text": "ok"}.get(mode, "ok")


class Handler(BaseHTTPRequestHandler):
    state_path = None

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _sse(self, events):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        for ev in events:
            self.wfile.write(ev.encode())
            self.wfile.flush()

    def do_GET(self):
        self._record({}, "GET")
        self._send(200, {"object": "list", "data": [{"id": "stub-model", "object": "model",
                                                       "created": 0, "owned_by": "stub"}],
                         "models": [{"name": "models/stub-model", "supportedGenerationMethods":
                                     ["generateContent"]}]})

    def _record(self, body, kind, extra=None):
        st = load(self.state_path)
        if st.get("log"):
            tools = body.get("tools")
            names = []
            for t in tools or []:
                if "functionDeclarations" in t:
                    names += [d["name"] for d in t["functionDeclarations"]]
                else:
                    names.append((t.get("function") or t).get("name"))
            with open(st["log"], "a") as f:
                f.write(json.dumps({"ts": time.time(), "path": self.path, "kind": kind,
                                    "n_tools": len(tools or []), "tools": names[:40],
                                    "tool_result_seen": has_tool_result(body),
                                    "excerpt": excerpt(body), **(extra or {})}) + "\n")
        return st

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        try:
            body = json.loads(raw or b"{}")
        except ValueError:
            body = {}
        st = load(self.state_path)
        name, schema = pick_shell(body.get("tools"))
        side = name is None and not has_tool_result(body)
        if side and st.get("classifier") in ("http500", "malformed"):
            self._record(body, "side-call", {"answered": st["classifier"]})
            if st["classifier"] == "http500":
                return self._send(500, {"error": {"message": "internal error", "type": "server_error"}})
            return self._send(200, b"<html>502 Bad Gateway</html>", "text/html")
        if has_tool_result(body) or side:
            action = ("final", side_call_text(st.get("classifier", "safe")) if side else "done.")
        else:
            action = ("tool", name, fill_args(schema, st["command"]))
        self._record(body, action[0], {"shell_tool": name, "args": action[2] if action[0] == "tool" else None})
        if ":generateContent" in self.path or ":streamGenerateContent" in self.path:
            return self._gemini(action, "streamGenerateContent" in self.path)
        if self.path.rstrip("/").endswith("/responses"):
            return self._responses(action, bool(body.get("stream")))
        return self._chat(action, bool(body.get("stream")), body.get("model", "stub-model"))

    # ---- OpenAI chat completions ------------------------------------------------------
    def _chat(self, action, stream, model):
        cid, now = "chatcmpl-" + uuid.uuid4().hex[:12], int(time.time())
        if action[0] == "tool":
            call = {"id": "call_" + uuid.uuid4().hex[:12], "type": "function",
                    "function": {"name": action[1], "arguments": json.dumps(action[2])}}
            msg, finish = {"role": "assistant", "content": None, "tool_calls": [call]}, "tool_calls"
        else:
            msg, finish = {"role": "assistant", "content": action[1]}, "stop"
        usage = {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
        if not stream:
            return self._send(200, {"id": cid, "object": "chat.completion", "created": now,
                                    "model": model, "choices": [{"index": 0, "message": msg,
                                                                 "finish_reason": finish}],
                                    "usage": usage})
        delta = dict(msg)
        if "tool_calls" in delta:
            delta["tool_calls"] = [dict(delta["tool_calls"][0], index=0)]
        chunk = lambda d, f: "data: " + json.dumps({"id": cid, "object": "chat.completion.chunk",  # noqa: E731
                                                    "created": now, "model": model,
                                                    "choices": [{"index": 0, "delta": d,
                                                                 "finish_reason": f}]}) + "\n\n"
        last = "data: " + json.dumps({"id": cid, "object": "chat.completion.chunk", "created": now,
                                      "model": model, "choices": [], "usage": usage}) + "\n\n"
        self._sse([chunk(delta, None), chunk({}, finish), last, "data: [DONE]\n\n"])

    # ---- OpenAI Responses API ---------------------------------------------------------
    def _responses(self, action, stream):
        rid = "resp_" + uuid.uuid4().hex[:12]
        if action[0] == "tool":
            item = {"type": "function_call", "id": "fc_" + uuid.uuid4().hex[:8],
                    "call_id": "call_" + uuid.uuid4().hex[:8], "name": action[1],
                    "arguments": json.dumps(action[2]), "status": "completed"}
        else:
            item = {"type": "message", "id": "msg_" + uuid.uuid4().hex[:8], "role": "assistant",
                    "status": "completed",
                    "content": [{"type": "output_text", "text": action[1], "annotations": []}]}
        resp = {"id": rid, "object": "response", "created_at": int(time.time()), "status": "completed",
                "model": "stub-model", "output": [item],
                "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}
        if not stream:
            return self._send(200, resp)
        ev = lambda t, d: f"event: {t}\ndata: {json.dumps(dict(d, type=t))}\n\n"  # noqa: E731
        evs = [ev("response.created", {"response": dict(resp, status="in_progress", output=[])}),
               ev("response.output_item.added", {"output_index": 0, "item": item})]
        if item["type"] == "message":
            evs.append(ev("response.output_text.delta", {"output_index": 0, "content_index": 0,
                                                         "item_id": item["id"], "delta": action[1]}))
        else:
            evs.append(ev("response.function_call_arguments.delta",
                          {"output_index": 0, "item_id": item["id"], "delta": item["arguments"]}))
            evs.append(ev("response.function_call_arguments.done",
                          {"output_index": 0, "item_id": item["id"], "arguments": item["arguments"]}))
        evs += [ev("response.output_item.done", {"output_index": 0, "item": item}),
                ev("response.completed", {"response": resp})]
        self._sse(evs)

    # ---- Gemini generateContent ---------------------------------------------------------
    def _gemini(self, action, stream):
        part = ({"functionCall": {"name": action[1], "args": action[2]}} if action[0] == "tool"
                else {"text": action[1]})
        resp = {"candidates": [{"content": {"role": "model", "parts": [part]},
                                "finishReason": "STOP", "index": 0}],
                "usageMetadata": {"promptTokenCount": 1, "candidatesTokenCount": 1,
                                  "totalTokenCount": 2}, "modelVersion": "stub-model"}
        if not stream:
            return self._send(200, resp)
        self._sse(["data: " + json.dumps(resp) + "\r\n\r\n"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--state", required=True)
    args = ap.parse_args()
    Handler.state_path = args.state
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"stub model on 127.0.0.1:{args.port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
