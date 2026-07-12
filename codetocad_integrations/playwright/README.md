# Playwright integration

Headless-browser screenshots, mainly used to capture `WebApp` control
panels for documentation (e.g. example READMEs). `screenshot_url` works
against any local URL if you need it for something else.

## Install

Playwright needs a downloaded browser binary in addition to the pip
package, so there's a second install step:

```
uv sync --extra playwright
uv run playwright install chromium
```

The `playwright install` step downloads a Chromium build (~150-300 MB,
cached under `~/.cache/ms-playwright`) and only needs to run once per
machine. On Linux you may also need `playwright install --with-deps
chromium` to pull in system libraries Chromium requires.

## Usage

```python
from codetocad import WebApp
from codetocad_integrations.playwright import screenshot_webapp

app = WebApp("robot lab").set_communication(communication)
app.add_slider("speed", target=motor, command="velocity_rpm", minimum=0, maximum=300)
...

screenshot_webapp(app, "images/gui.png")
```

`screenshot_webapp` serves the app on a background thread, waits for it
to come up, and saves a PNG once the page has rendered. It's a thin
wrapper around `screenshot_url`, which you can call directly against any
URL (e.g. `localhost` pages served by other tools) if you don't have a
`WebApp` instance.
