"""Imported automatically when this directory is on PYTHONPATH: reroutes calls
to the decision-model hosts to the local fault server (FI_PORT) over plain
HTTP. Gate code runs unmodified. Covers urllib, requests, and httpx."""

import os
import urllib.parse

_HOSTS = {"api.typesafe.ai", "ai-gateway.vercel.sh", "openrouter.ai"}
_PORT = os.environ.get("FI_PORT")


def _rewrite(url):
    try:
        p = urllib.parse.urlsplit(str(url))
    except ValueError:
        return None
    if p.hostname not in _HOSTS:
        return None
    return urllib.parse.urlunsplit(("http", f"127.0.0.1:{_PORT}", p.path, p.query, ""))


if _PORT:
    import urllib.request as _ur

    _orig_init = _ur.Request.__init__

    def _req_init(self, url, *a, **kw):
        _orig_init(self, _rewrite(url) or url, *a, **kw)

    _ur.Request.__init__ = _req_init

    _orig_open = _ur.OpenerDirector.open

    def _open(self, fullurl, *a, **kw):
        if isinstance(fullurl, str):
            fullurl = _rewrite(fullurl) or fullurl
        return _orig_open(self, fullurl, *a, **kw)

    _ur.OpenerDirector.open = _open

    import importlib.abc
    import importlib.machinery
    import sys

    def _patch_requests(mod):
        orig = mod.Session.request

        def request(self, method, url, *a, **kw):
            return orig(self, method, _rewrite(url) or url, *a, **kw)

        mod.Session.request = request

    def _patch_httpx(mod):
        for cls_name in ("Client", "AsyncClient"):
            cls = getattr(mod, cls_name)
            orig = cls.build_request

            def build_request(self, method, url, *a, _orig=orig, **kw):
                return _orig(self, method, _rewrite(url) or url, *a, **kw)

            cls.build_request = build_request

    _PATCHES = {"requests": _patch_requests, "httpx": _patch_httpx}

    class _Finder(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name not in _PATCHES:
                return None
            sys.meta_path.remove(self)
            try:
                spec = importlib.util.find_spec(name)
            finally:
                sys.meta_path.insert(0, self)
            if spec is None or spec.loader is None:
                return None
            loader = spec.loader
            orig_exec = loader.exec_module

            def exec_module(module, _orig=orig_exec, _name=name):
                _orig(module)
                _PATCHES[_name](module)

            loader.exec_module = exec_module
            return spec

    import importlib.util
    sys.meta_path.insert(0, _Finder())
