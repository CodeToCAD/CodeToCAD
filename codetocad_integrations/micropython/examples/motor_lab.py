"""Motor lab: an ESP32 driving a brushed DC motor with encoder feedback.

Wiring:
- DRV8871 H-bridge: PWM on GPIO5, direction on GPIO18
- quadrature encoder: A on GPIO32, B on GPIO33
- potentiometer (throttle readback): wiper on GPIO34

Run once with UPLOAD=1 to flash the generated MicroPython firmware, then
run normally to open the control panel in the browser::

    UPLOAD=1 uv run python motor_lab.py   # flash main.py via mpremote
    uv run python motor_lab.py            # open the WebApp
"""

import os

from codetocad import (
    Microcontroller,
    MicrocontrollerBoard,
    SerialCommunication,
    WebApp,
)
from codetocad.mixins import DCMotorMixin, EncoderMixin, SensorMixin

PORT = os.environ.get("PORT", "/dev/tty.usbserial-0001")


class GearMotor(DCMotorMixin):
    nominal_voltage = 12.0
    no_load_speed_rpm = 200


class MotorEncoder(EncoderMixin):
    counts_per_revolution = 2048
    sample_rate_hz = 20.0


class Throttle(SensorMixin):
    sample_rate_hz = 10.0


motor = GearMotor()
encoder = MotorEncoder()
throttle = Throttle()

communication = SerialCommunication(PORT)

mcu = Microcontroller("motor-lab", board=MicrocontrollerBoard.ESP32)
mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
mcu.bind_sensor(encoder, name="enc", a=32, b=33)
mcu.bind_sensor(throttle, name="throttle", pin=34)
mcu.set_communication(communication)

if os.environ.get("UPLOAD"):
    mcu.upload()
    raise SystemExit(f"Firmware uploaded over {PORT}")

app = WebApp("Motor lab").set_communication(communication)
app.add_slider("speed (rpm)", target=motor, command="velocity_rpm",
               minimum=0, maximum=200)
app.add_button("stop", target=motor, value={"stop": True})
app.add_gauge("throttle (V)", source=throttle, maximum=3.3, units="V")
app.add_plot("measured rpm", source=encoder)
app.run()
