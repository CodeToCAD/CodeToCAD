"""Generate images/turtlebot_gui.png: drive the turtlebot in a background
thread and screenshot the WebApp control panel with Playwright.

    python shoot_turtlebot_gui.py

Requires the mujoco, nicegui, and playwright extras (see
codetocad_integrations/playwright/README.md for the browser-binary
install step).
"""
import os
import sys
import threading
from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXAMPLE_DIR))

from turtlebot_diff_drive import (
    MOTOR_NO_LOAD_RPM,
    build_turtlebot,
    drive,
    make_app,
    make_microcontroller,
    make_simulation,
    wire_emulation,
)

from codetocad_integrations.playwright import screenshot_webapp

chassis, left_wheel, right_wheel = build_turtlebot()
sim = make_simulation(chassis)
mcu, left_encoder, right_encoder = make_microcontroller(left_wheel, right_wheel)
emulator = wire_emulation(sim, mcu)
emulator.communication.connect()
left_wheel.set_velocity(0.5 * MOTOR_NO_LOAD_RPM)
right_wheel.set_velocity(0.5 * MOTOR_NO_LOAD_RPM)

stop = threading.Event()


def simulation_loop():
    while not stop.is_set():
        drive(sim, emulator, 0.25, realtime=True)


threading.Thread(target=simulation_loop, daemon=True).start()

app = make_app(emulator.communication, left_wheel, right_wheel, left_encoder, right_encoder)
out_png = IMAGES_DIR / "turtlebot_gui.png"
screenshot_webapp(
    app, str(out_png), startup_wait_seconds=3.0, capture_wait_seconds=2.0,
    width=900, height=900,
)
print("saved", out_png)
os._exit(0)  # the WebApp server thread has no clean shutdown path
