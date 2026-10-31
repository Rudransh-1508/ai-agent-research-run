// Preloaded with NODE_OPTIONS=--require: reroutes calls to the decision-model
// hosts to the local fault server (FI_PORT) over plain HTTP. Gate code runs
// unmodified. Everything else passes through untouched.
"use strict";
const http = require("node:http");
const https = require("node:https");

const HOSTS = new Set(["api.typesafe.ai", "ai-gateway.vercel.sh", "openrouter.ai"]);
const PORT = process.env.FI_PORT;
if (!PORT) return;
const LOCAL = `http://127.0.0.1:${PORT}`;

function rewrite(u) {
  try {
    const url = new URL(String(u));
    if (!HOSTS.has(url.hostname)) return null;
    return LOCAL + url.pathname + url.search;
  } catch {
    return null;
  }
}

const origFetch = globalThis.fetch;
if (origFetch) {
  globalThis.fetch = function (input, init) {
    const raw = typeof input === "string" || input instanceof URL ? input : input && input.url;
    const target = raw && rewrite(raw);
    if (!target) return origFetch.call(this, input, init);
    if (typeof input === "string" || input instanceof URL) return origFetch.call(this, target, init);
    return origFetch.call(this, new Request(target, input), init);
  };
}

function wrap(mod, name) {
  const orig = mod[name];
  mod[name] = function (a, b, c) {
    let opts = a;
    if (typeof a === "string" || a instanceof URL) {
      const target = rewrite(a);
      if (target) return http[name](target, typeof b === "function" ? undefined : b, typeof b === "function" ? b : c);
      return orig.call(this, a, b, c);
    }
    if (opts && HOSTS.has(opts.hostname || String(opts.host || "").split(":")[0])) {
      const o = Object.assign({}, opts, { protocol: "http:", hostname: "127.0.0.1", host: undefined, port: Number(PORT), agent: undefined });
      return http[name](o, b, c);
    }
    return orig.call(this, a, b, c);
  };
}
wrap(https, "request");
wrap(https, "get");
