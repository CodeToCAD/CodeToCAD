# Controls: microcontroller, apps, and transports

This ties parts-as-sensors/actuators to a `Microcontroller` and a control-panel
app, over a shared `Communication`. The same setup drives real hardware or a
physics simulation — only the transport/emulator changes.

## The pattern

1. Make a part a sensor/actuator by inheriting a mixin (see [core-classes.md](../core-classes.md)).
2. Bind it to `Microcontroller` pins.
3. Give the MCU a `Communication`.
4. Bind an `AppBase` (`WebApp`/`PythonApp`/`RerunApp`) to the **same**
   `Communication` so both ends speak the same JSON-lines wire protocol.

```python
from codetocad import (Microcontroller, MicrocontrollerBoard,
                       SerialCommunication, WebApp)
from codetocad.mixins import DCMotorMixin, EncoderMixin

class GearMotor(DCMotorMixin):
    no_load_speed_rpm = 200

motor, encoder = GearMotor(), EncoderMixin()
mcu = Microcontroller("motor-lab", board=MicrocontrollerBoard.ESP32)
mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
mcu.bind_sensor(encoder, name="enc", a=32, b=33)
mcu.set_communication(SerialCommunication("/dev/ttyUSB0"))

app = WebApp("motor lab").set_communication(mcu.communication)
app.add_slider("speed (rpm)", target=motor, command="velocity_rpm", maximum=200)
app.add_plot("measured rpm", source=encoder)
app.run()
```

## Microcontroller (`codetocad`)

- `Microcontroller(name, board=MicrocontrollerBoard.ESP32)`.
- `bind_sensor(part, name=..., **pins)` / `bind_actuator(part, name=..., **pins)`.
- `set_communication(comm)`; `mcu.communication` is the bound instance.
- `sensors` / `actuators` / `get_binding(name)`.
- `generate_firmware()` → firmware source; `upload(port=...)` flashes it.
- Buses `I2CBus`/`SPIBus`/`UARTBus` for bus-attached peripherals.

## Apps (`AppBase`)

Controls: `add_slider`, `add_button`, `add_toggle`, `add_gauge`, `add_plot`,
`add_image`, `add_label`. `target=`/`command=` bind an actuator; `source=` binds
a sensor. Then `.run(...)`:

- **`WebApp`** — browser page. `uv sync --extra nicegui`. Served by
  `codetocad_integrations.nicegui.serve`. `run(host="0.0.0.0", port=8080)`.
- **`PythonApp`** — native window (nicegui native mode).
- **`RerunApp`** — streams telemetry to the [Rerun](https://rerun.io) viewer.
  `uv sync --extra rerun`; served by `codetocad_integrations.rerun.serve`.

All three take the same `Communication` as the MCU.

## Communication / transports

`Communication` subclasses select the wire:

- `SerialCommunication(port)` — over the **pyserial** transport
  (`codetocad_integrations.pyserial`: `SerialTransport`, `list_ports()`).
  Install `uv sync --extra pyserial`.
- `MqttCommunication(...)` — over **mqtt**
  (`codetocad_integrations.mqtt.MqttTransport`, paho). `uv sync --extra mqtt`.
- `WifiCommunication` / `BluetoothCommunication` — wireless transports.
- `EmulatedCommunication` — no hardware; pairs with `EmulatedMicrocontroller`.

## Emulation (drive a simulation instead of hardware)

`EmulatedMicrocontroller` runs the MCU's control logic in-process against a
physics `Simulation` instead of a real board. Swap the emulator's
`EmulatedCommunication` for a `SerialCommunication` and the *same* app drives
physical hardware — that swap is the only change. This is the backbone of the
robotics examples ([robotics.md](robotics.md)).

## VESC BLDC — `codetocad_integrations.vesc`

`VESCMotor` (a `BLDCMotorMixin`) talks to a real VESC ESC over serial (pyvesc).
`uv sync --extra vesc`.

## MicroPython firmware — `codetocad_integrations.micropython`

`generate_main_py(...)` emits a `main.py` for the bound MCU; `upload(...)` copies
it to a MicroPython board. `uv sync --extra micropython`.

## Playwright (screenshots) — `codetocad_integrations.playwright`

Headless screenshots of a running WebApp or any URL: `screenshot_webapp(app, ...)`,
`screenshot_url(url, ...)`. Useful for docs/CI captures of control panels.
`uv sync --extra playwright`.
