"""micropython integration: generate and upload firmware for a Microcontroller.

``generate_main_py(mcu)`` turns a ``codetocad.Microcontroller`` definition
(its pin bindings and communication channel) into a device-side agent
script that speaks the codetocad wire protocol:

- MicroPython boards (ESP32, ESP8266, Raspberry Pi Pico) get a ``main.py``
  using the ``machine`` module,
- Python boards (Raspberry Pi) get a CPython script using gpiozero.

``upload(mcu, port=...)`` flashes the generated ``main.py`` onto a
MicroPython board with `mpremote <https://docs.micropython.org/en/latest/reference/mpremote.html>`_
(``uv sync --extra micropython``)::

    mcu = Microcontroller("driver", board=MicrocontrollerBoard.ESP32)
    mcu.bind_actuator(motor, name="wheel", pwm_pin=5, dir_pin=18)
    mcu.set_communication(SerialCommunication("/dev/ttyUSB0"))
    mcu.upload()                      # calls upload(mcu) under the hood

Driver wiring expected by the generated firmware. GPIO drivers take pins
directly; bus drivers take ``bus=`` (an ``I2CBus``/``SPIBus``/``UARTBus``
shared between devices) plus ``address=`` for I2C or ``cs=`` for SPI:

=================  ====================  =========================================
driver             attachment            notes
=================  ====================  =========================================
analog             pin                   ADC input; telemetry is volts
digital_in         pin                   telemetry is 0/1
current            pin                   ADC volts; convert with CurrentSensorMixin
encoder            a, b                  quadrature; telemetry {"count", "rpm"}
imu_mpu6050        bus+address           MPU6050; {"accel", "gyro"} (also accepts
                                         legacy sda/scl pins on MicroPython)
i2c_register       bus+address           generic register read; params
                                         {"register", "length", "scale", "signed"}
current_ina219     bus+address           INA219 shunt monitor; telemetry is amps;
                                         params {"shunt_ohms": 0.1}
adc_mcp3008        bus(SPI)+cs           MCP3008 ADC; params {"channel", "vref"};
                                         on a Pi, cs must be CE0 (GPIO8) or CE1
                                         (GPIO7)
pwm                pin                   command value 0..1 duty
digital_out        pin                   command value 0/1
servo              pin                   command value degrees 0..180
dc_motor           pwm, dir              H-bridge (L298N/TB6612/DRV8871); commands
                                         {"duty"}, {"velocity_rpm"}, {"stop"}
stepper            step, dir             A4988/DRV8825/TMC2209; commands
                                         {"steps"}, {"position_steps"}
pwm_pca9685        bus+address           PCA9685 16-channel PWM; params
                                         {"channel", "frequency_hz"}
servo_pca9685      bus+address           servo on a PCA9685 channel; params
                                         {"channel"}
dc_motor_drv8830   bus+address           DRV8830 I2C motor driver; same commands
                                         as dc_motor
vesc_uart          bus(UART)             VESC over UART; {"duty"},
                                         {"velocity_rpm"} (erpm via pole_pairs),
                                         {"current_amps"}, {"stop"}
=================  ====================  =========================================

Raspberry Pi (Python runtime) notes: I2C drivers need ``smbus2`` and UART
drivers need ``pyserial`` on the device; analog inputs require an MCP3008
since the Pi has no on-board ADC.
"""

from codetocad_integrations.micropython.firmware import (
    generate_main_py,
    upload,
)

__all__ = ["generate_main_py", "upload"]
