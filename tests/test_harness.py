"""
SEG301 Exam Prep Portal - E2E Test Harness
Provides Headless Edge CDP Automation, CSS/JS AST Analysis, and TAP Reporting.
"""

import asyncio
import http.server
import json
import os
import re
import socket
import socketserver
import subprocess
import sys
import threading
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import tornado.websocket

# Configure UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_FILE = os.path.join(PROJECT_ROOT, "css", "style.css")
JS_FILE = os.path.join(PROJECT_ROOT, "js", "app.js")
HTML_FILE = os.path.join(PROJECT_ROOT, "index.html")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress HTTP server noise

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


class CSSAnalyzer:
    """Static and structural analyzer for CSS design tokens, keyframes, and rules."""

    def __init__(self, css_path: str = CSS_FILE):
        self.css_path = css_path
        self.raw_css = ""
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                self.raw_css = f.read()

    def get_root_variable(self, var_name: str) -> Optional[str]:
        m = re.search(rf'--{re.escape(var_name.lstrip("-"))}\s*:\s*([^;]+);', self.raw_css)
        return m.group(1).strip() if m else None

    def has_rule_with_selector(self, selector_pattern: str) -> bool:
        # Matches selector before an opening brace
        pattern = rf'(?:^|\}})[^{{\}}]*?({selector_pattern})[^{{\}}]*?\{{'
        return bool(re.search(pattern, self.raw_css, re.MULTILINE))

    def get_rule_content(self, selector_pattern: str) -> List[str]:
        contents = []
        for match in re.finditer(rf'([^{{}}\n][^{{}}]*?{selector_pattern}[^{{}}]*?)\{{([^}}]+)\}}', self.raw_css):
            contents.append(match.group(2).strip())
        return contents

    def get_keyframes(self, anim_name: str) -> Optional[str]:
        m = re.search(rf'@keyframes\s+{re.escape(anim_name)}\s*\{{([^}}]+(?:\{{[^}}]*\}}[^}}]*)*)\}}', self.raw_css)
        return m.group(1).strip() if m else None

    def get_reduced_motion_block(self) -> Optional[str]:
        m = re.search(r'@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)\s*\{([\s\S]*?)(?:\}\s*\}|\}\s*(?=@media|\Z))', self.raw_css)
        if not m:
            m = re.search(r'@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)\s*\{([\s\S]*)\}', self.raw_css)
        return m.group(1).strip() if m else None

    def find_unscoped_transition_all(self) -> List[str]:
        """Find instances of `transition: all` or `transition:all` in css."""
        matches = []
        for line_num, line in enumerate(self.raw_css.splitlines(), start=1):
            if re.search(r'transition\s*:\s*all\b', line):
                matches.append(f"Line {line_num}: {line.strip()}")
        return matches


class JSAnalyzer:
    """Static analyzer for JS controllers and contracts."""

    def __init__(self, js_path: str = JS_FILE):
        self.js_path = js_path
        self.raw_js = ""
        if os.path.exists(js_path):
            with open(js_path, "r", encoding="utf-8") as f:
                self.raw_js = f.read()

    def contains(self, pattern: str) -> bool:
        return bool(re.search(pattern, self.raw_js))


@dataclass
class TestResult:
    test_id: str
    feature: str
    tier: str
    description: str
    passed: bool
    message: str = ""
    duration_ms: float = 0.0


class TestReporter:
    def __init__(self):
        self.results: List[TestResult] = []

    def record(self, test_id: str, feature: str, tier: str, description: str, passed: bool, message: str = "", duration_ms: float = 0.0):
        res = TestResult(test_id, feature, tier, description, passed, message, duration_ms)
        self.results.append(res)
        status_sym = "✓ PASS" if passed else "✗ FAIL"
        if not passed:
            print(f"[{tier}] {test_id} ({feature}): {status_sym} - {description}")
            if message:
                print(f"    Reason: {message}")

    def generate_tap(self) -> str:
        lines = ["TAP version 13", f"1..{len(self.results)}"]
        for idx, r in enumerate(self.results, start=1):
            status = "ok" if r.passed else "not ok"
            desc = f"{r.test_id} - [{r.tier}] [{r.feature}] {r.description}"
            if r.passed:
                lines.append(f"{status} {idx} - {desc}")
            else:
                lines.append(f"{status} {idx} - {desc}")
                lines.append("  ---")
                lines.append(f"  message: {json.dumps(r.message)}")
                lines.append(f"  tier: {r.tier}")
                lines.append(f"  feature: {r.feature}")
                lines.append("  ...")
        return "\n".join(lines)

    def print_summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        print("\n" + "=" * 70)
        print("E2E TEST EXECUTION SUMMARY")
        print("=" * 70)

        # Tier Breakdown
        tiers = sorted(list(set(r.tier for r in self.results)))
        for t in tiers:
            t_res = [r for r in self.results if r.tier == t]
            t_pass = sum(1 for r in t_res if r.passed)
            t_fail = len(t_res) - t_pass
            print(f"  {t:<8}: {t_pass:>3} passed / {len(t_res):>3} total ({'100%' if t_fail==0 else f'{t_pass*100//len(t_res)}%'})")

        print("-" * 70)
        print(f"TOTAL TESTS : {total}")
        print(f"PASSED      : {passed}")
        print(f"FAILED      : {failed}")
        print(f"SUCCESS RATE: {(passed / total * 100):.1f}%" if total > 0 else "0%")
        print("=" * 70 + "\n")


class EdgeCDPDriver:
    """Manages Headless Edge with Chrome DevTools Protocol over tornado.websocket."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.http_port = find_free_port()
        self.cdp_port = find_free_port()
        self.http_server: Optional[socketserver.TCPServer] = None
        self.http_thread: Optional[threading.Thread] = None
        self.edge_proc: Optional[subprocess.Popen] = None
        self.ws: Optional[tornado.websocket.WebSocketClientConnection] = None
        self.msg_id = 0
        self.console_errors: List[str] = []
        self.loop = asyncio.new_event_loop()

    def start(self):
        # 1. Start HTTP server
        self.http_server = socketserver.TCPServer(('127.0.0.1', self.http_port), QuietHTTPHandler)
        self.http_thread = threading.Thread(target=self.http_server.serve_forever, daemon=True)
        self.http_thread.start()

        # 2. Launch Edge headless
        cmd = [
            EDGE_EXE,
            "--headless=new" if self.headless else "",
            f"--remote-debugging-port={self.cdp_port}",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1280,800",
            f"http://127.0.0.1:{self.http_port}/index.html"
        ]
        cmd = [c for c in cmd if c]
        self.edge_proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Connect to CDP tab via WebSocket
        self.loop.run_until_complete(self._connect_cdp())

    async def _connect_cdp(self):
        retries = 25
        ws_url = None
        while retries > 0:
            try:
                res = urllib.request.urlopen(f"http://127.0.0.1:{self.cdp_port}/json/list", timeout=1)
                tabs = json.loads(res.read().decode('utf-8'))
                for tab in tabs:
                    if tab.get('type') == 'page':
                        ws_url = tab.get('webSocketDebuggerUrl')
                        break
                if ws_url:
                    break
            except Exception:
                pass
            await asyncio.sleep(0.2)
            retries -= 1

        if not ws_url:
            raise RuntimeError("Failed to connect to Microsoft Edge CDP debugger target")

        self.ws = await tornado.websocket.websocket_connect(ws_url)

        # Enable runtime & log domains
        await self._send_cdp("Runtime.enable")
        await self._send_cdp("Page.enable")
        await self._send_cdp("DOM.enable")
        await self._send_cdp("CSS.enable")

        # Wait for document ready
        await asyncio.sleep(1.0)

    async def _send_cdp(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.msg_id += 1
        curr_id = self.msg_id
        payload = {"id": curr_id, "method": method, "params": params or {}}
        await self.ws.write_message(json.dumps(payload))

        while True:
            raw = await self.ws.read_message()
            if not raw:
                raise RuntimeError("CDP WebSocket connection closed")
            data = json.loads(raw)
            if data.get("id") == curr_id:
                if "error" in data:
                    raise RuntimeError(f"CDP Error ({method}): {data['error']}")
                return data.get("result", {})
            elif data.get("method") == "Runtime.consoleAPICalled":
                params = data.get("params", {})
                if params.get("type") in ("error", "assert"):
                    msg = " ".join(str(arg.get("value", "")) for arg in params.get("args", []))
                    self.console_errors.append(msg)

    def eval_js(self, expression: str, await_promise: bool = False) -> Any:
        async def _eval():
            params = {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise
            }
            res = await self._send_cdp("Runtime.evaluate", params)
            result_obj = res.get("result", {})
            if result_obj.get("subtype") == "error":
                raise RuntimeError(f"JavaScript Error: {result_obj.get('description')}")
            return result_obj.get("value")

        return self.loop.run_until_complete(_eval())

    def get_computed_style(self, selector: str, pseudo: str = "") -> Dict[str, str]:
        js_code = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (!el) return null;
            const style = window.getComputedStyle(el, {json.dumps(pseudo) if pseudo else "null"});
            return {{
                opacity: style.opacity,
                transform: style.transform,
                transition: style.transition,
                transitionDuration: style.transitionDuration,
                transitionProperty: style.transitionProperty,
                animation: style.animation,
                animationName: style.animationName,
                animationDuration: style.animationDuration,
                outline: style.outline,
                outlineColor: style.outlineColor,
                outlineStyle: style.outlineStyle,
                outlineWidth: style.outlineWidth,
                boxShadow: style.boxShadow,
                cursor: style.cursor,
                visibility: style.visibility,
                display: style.display,
                willChange: style.willChange,
                overflowX: style.overflowX
            }};
        }})()
        """
        return self.eval_js(js_code) or {}

    def get_bounding_rect(self, selector: str) -> Dict[str, float]:
        js_code = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {{ top: r.top, left: r.left, width: r.width, height: r.height, bottom: r.bottom, right: r.right }};
        }})()
        """
        return self.eval_js(js_code) or {}

    def click(self, selector: str):
        js_code = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (el) {{
                el.click();
                return true;
            }}
            return false;
        }})()
        """
        success = self.eval_js(js_code)
        # Small tick for UI update
        self.loop.run_until_complete(asyncio.sleep(0.08))
        return success

    def focus(self, selector: str):
        js_code = f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (el) {{
                el.focus();
                return true;
            }}
            return false;
        }})()
        """
        return self.eval_js(js_code)

    def scroll_to(self, y: int):
        js_code = f"""
        (() => {{
            window.scrollTo(0, {y});
            window.dispatchEvent(new Event('scroll'));
        }})()
        """
        self.eval_js(js_code)
        self.loop.run_until_complete(asyncio.sleep(0.15))

    def set_reduced_motion(self, reduce: bool = True):
        async def _set_media():
            await self._send_cdp("Emulation.setEmulatedMedia", {
                "media": "screen",
                "features": [{"name": "prefers-reduced-motion", "value": "reduce" if reduce else "no-preference"}]
            })
            await asyncio.sleep(0.1)

        self.loop.run_until_complete(_set_media())

    def stop(self):
        try:
            if self.ws:
                self.ws.close()
        except Exception:
            pass

        try:
            if self.edge_proc:
                self.edge_proc.terminate()
                self.edge_proc.wait(timeout=3)
        except Exception:
            pass

        try:
            if self.http_server:
                self.http_server.shutdown()
                self.http_server.server_close()
        except Exception:
            pass

        try:
            self.loop.close()
        except Exception:
            pass
