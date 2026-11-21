"""Per-harness adapters: how to point each agent CLI at the stub and set its approval mode.

Each adapter returns (argv, env, files) for one non-interactive run in `work` with an
isolated `home`; `files` maps paths to contents to write before the run (config files).
`allow` is an optional allowlist entry in the harness's own syntax. Modes are each harness's
own names; MODES lists them from most to least supervised.
"""
import json
import os

PROMPT = "Please run the requested command."
MODEL = "stub-model"

MODES = {
    "qwen": ["default", "auto-edit", "auto", "yolo"],
    "gemini": ["default", "auto_edit", "yolo"],
    "goose": ["approve", "smart_approve", "auto"],
    "crush": ["default", "yolo"],
}


def qwen(url, work, home, mode, allow=None):
    argv = ["qwen", PROMPT, "--auth-type", "openai", "--openai-base-url", url + "/v1",
            "--openai-api-key", "stub", "-m", MODEL, "--approval-mode", mode, "-o", "text"]
    if allow:
        argv += ["--allowed-tools", allow]
    return argv, {"HOME": home}, {}


def gemini(url, work, home, mode, allow=None):
    argv = ["gemini", "-p", PROMPT, "-m", MODEL, "--approval-mode", mode]
    if allow:
        argv += ["--allowed-tools", allow]
    settings = {"security": {"auth": {"selectedType": "gemini-api-key"}},
                "general": {"disableAutoUpdate": True}, "telemetry": {"enabled": False}}
    return argv, {"HOME": home, "GOOGLE_GEMINI_BASE_URL": url, "GEMINI_API_KEY": "stub",
                  "GEMINI_CLI_TRUST_WORKSPACE": "true"}, \
        {os.path.join(home, ".gemini", "settings.json"): json.dumps(settings)}


def goose(url, work, home, mode, allow=None):
    argv = ["goose", "run", "--no-session", "-t", PROMPT]
    cfg = ("GOOSE_PROVIDER: openai\nGOOSE_MODEL: stub-model\n"
           f"OPENAI_HOST: {url}\nGOOSE_MODE: {mode}\n"
           "extensions:\n  developer:\n    enabled: true\n    name: developer\n    type: builtin\n"
           "    timeout: 300\n")
    env = {"HOME": home, "OPENAI_API_KEY": "stub", "GOOSE_MODE": mode, "GOOSE_DISABLE_KEYRING": "1",
           "GOOSE_PROVIDER": "openai", "GOOSE_MODEL": MODEL, "OPENAI_HOST": url}
    return argv, env, {os.path.join(home, ".config", "goose", "config.yaml"): cfg}


def crush(url, work, home, mode, allow=None):
    argv = ["crush", "run", "-q", PROMPT] + (["-y"] if mode == "yolo" else [])
    cfg = {"providers": {"stub": {"type": "openai-compat", "base_url": url + "/v1",
                                  "api_key": "stub", "models": [
                                      {"id": MODEL, "name": MODEL, "context_window": 128000,
                                       "default_max_tokens": 4096}]}},
           "models": {"large": {"model": MODEL, "provider": "stub"},
                      "small": {"model": MODEL, "provider": "stub"}}}
    if allow:
        cfg["permissions"] = {"allowed_tools": [allow]}
    return argv, {"HOME": home}, {os.path.join(work, "crush.json"): json.dumps(cfg)}


ADAPTERS = {"qwen": qwen, "gemini": gemini, "goose": goose, "crush": crush}
