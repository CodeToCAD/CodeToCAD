"""Playwright integration: headless-browser screenshots.

Mainly used to capture ``WebApp`` control panels for documentation (e.g.
example READMEs), but ``screenshot_url`` works against any local URL.

Requires the playwright extra and a downloaded browser binary::

    uv sync --extra playwright
    uv run playwright install chromium
"""

from __future__ import annotations

import threading
import time
from pathlib import Path


def screenshot_url(
    url: str,
    out_path: str | Path,
    *,
    width: int = 1280,
    height: int = 800,
    wait_seconds: float = 1.0,
    full_page: bool = True,
) -> Path:
    """Load ``url`` in headless Chromium and save a PNG screenshot.
    ``full_page`` captures the whole scrollable page rather than just the
    ``width``x``height`` viewport (the default, since docs screenshots
    usually want the entire control panel)."""
    from playwright.sync_api import sync_playwright

    out_path = Path(out_path)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url)
        if wait_seconds:
            page.wait_for_timeout(wait_seconds * 1000)
        page.screenshot(path=str(out_path), full_page=full_page)
        browser.close()
    return out_path


def screenshot_webapp(
    app,
    out_path: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8080,
    width: int = 1280,
    height: int = 800,
    startup_wait_seconds: float = 2.0,
    capture_wait_seconds: float = 1.0,
) -> Path:
    """Serve a ``codetocad.apps.WebApp`` on a background thread and
    screenshot it once it's up. The server thread is left running as a
    daemon; exit the process (or ``os._exit``) once done with it."""
    thread = threading.Thread(
        target=lambda: app.run(host=host, port=port, show=False), daemon=True
    )
    thread.start()
    time.sleep(startup_wait_seconds)
    return screenshot_url(
        f"http://{host}:{port}/",
        out_path,
        width=width,
        height=height,
        wait_seconds=capture_wait_seconds,
    )


__all__ = ["screenshot_url", "screenshot_webapp"]
