# ASITiger — A Python interface for ASI Tiger Controllers
![Build and release](https://github.com/System1Bio/asitiger/workflows/Build%20and%20release/badge.svg)

This is a Python package which provides a thin interface for communicating with [ASI TG-1000 "Tiger" Controllers](http://www.asiimaging.com/controllers/tiger-controller/). This package is concerned with making low-level interactions with Tiger Controllers easier by providing Python-native arguments to commands, and by parsing out convoluted responses and errors into nicer Python primitives.

Most methods map directly onto the identically named serial command described in the [ASI serial commands documentation](http://asiimaging.com/docs/products/tiger#serial_commands). Some methods—such as `axes`—build upon other commands to provide a more useful interface over somewhat-cryptic serial responses.

## Caveats
This package is very new and therefore has very few commands actually implemented. I also don't have access to every single ASI Tiger card to be able to test all commands in the serial API. If you'd like more commands added, please open an issue or PR.

For commands which this package doesn't expose an explicit method for yet, you may be able to get away with using the `TigerController#send_command(cmd)` method, which will allow you to send any arbitrary commands, and knows how to raise exceptions for each known failure response.

## Installation
This package is available on PyPI:

```shell
$ pip install asitiger
```
Note: This package has only been tested on Linux, if you run into issues on other operating systems, please open an issue.

## Usage
Commands are represented by methods on an `asitiger.TigerController` object, which can be created from the serial port / COM device it's connected to:

```python
from asitiger.tigercontroller import TigerController

tiger = TigerController.from_serial_port("/dev/ttyS0")

# When done, close the serial connection
tiger.connection.disconnect()
```

## Examples
Here are a few examples showing some of the things you can do. These examples assume you have `TigerController` object named `tiger`, like shown in the **Usage** section.

### Check if any motors are busy
You can check to see if any motors are active, and wait for all motors to become idle:

```python
tiger.status() # <Status.IDLE: 'N'>
tiger.is_busy() # True
tiger.wait_until_idle() # Blocks until every motor is idle
tiger.is_busy() # False
```

### Check and set axis speed
Speeds can be get/set through the `speed` method:

```python
tiger.speed({"X": "?", "Y": "?"})
# {'X': '29.998830', 'Y': '29.998830'}

tiger.speed({"X": 11})

tiger.speed({"X": "?"})
# {'X': '11.000030'}
```

### Move one or more axes
One or more axes can be moved at once, and moves can be sequenced with waits in between:

```python
tiger.move({"X": 50000, "Y": 0})
tiger.wait_until_idle()
tiger.move_relative({"X": -10000, "Y": -20000})
tiger.wait_until_idle()
tiger.move_relative({"X": -10000, "Y": -20000})
```

### Change LED intensity
You can change the intensity of the default LED (on your XYStage card) or directly address a TGLED card:

```python
# Set the default LED to 75% intensity
tiger.led({"X": 75})

# For a TGLED card (with card address 7)
# Set the 1st and 4th LED channels to 100% intensity, and turn all other channels off
tiger.led({"X": 100, "Y": 0, "Z": 0, "F": 100}, card_address=7)
```

### Lock or unlock a well plate
To change the position of a servo or solenoid well plate lock insert, use the higher-level `set_plate_lock` method, for lower-level control, you can use the `secure` method:

```python
from asitiger.secure import SecurePosition

# Unlock a plate (servo or solenoid)
tiger.set_plate_lock(SecurePosition.UNLOCKED, card_address=2)

# Lock a plate (servo or solenoid)
tiger.set_plate_lock(SecurePosition.LOCKED, card_address=2)

# Set the lock to a halfway position (servo only)
tiger.set_plate_lock(0.5)

# Set the auto-lock time to 3 minutes:
tiger.secure({"F": 3})
```

### Inspect available axes
You can inspect which cards/axes are installed, or query for axes on specific cards via the optional `card_address` keyword arg:

```python
tiger.axes()

# [AxisInfo(label='X', type=<Type.XY_MOTOR: 'x'>, address='1', address_hex='31'),
#  AxisInfo(label='Y', type=<Type.XY_MOTOR: 'x'>, address='1', address_hex='31'),
#  AxisInfo(label='Z', type=<Type.Z_MOTOR: 'z'>, address='2', address_hex='32'),
#  AxisInfo(label='S', type=<Type.SLIDER: 'f'>, address='2', address_hex='32'),
#  AxisInfo(label='O', type=<Type.TURRET: 'o'>, address='3', address_hex='33'),
#  AxisInfo(label='L', type=<Type.MULTI_LED: 'i'>, address='7', address_hex='37')]
```

### Check the detailed status of axes
Here the statuses of axes `X` and `O` are checked at the same time:

```python
x_axis_status, turret_status = tiger.rdstat(["X", "O"])

print(x_axis_status)

# AxisStatus(
#   status=<Status.IDLE: 'N'>,
#   enabled=<AxisEnabledStatus.ENABLED: 1>,
#   motor=<MotorStatus.INACTIVE: 0>,
#   joystick=<JoystickStatus.ENABLED: 1>,
#   ramping=<RampingStatus.NOT_RAMPING: 0>,
#   ramping_direction=<RampingDirection.DOWN: 0>,
#   upper_limit=<LimitStatus.OPEN: 0>,
#   lower_limit=<LimitStatus.OPEN: 0>
# )
```

### Send commands manually
If a command you want to send isn't currently supported as a first-class method, or you just want to send commands directly as strings:

```python
tiger.send_command("CDATE")
# 'Apr 30 2019:08:48:59'
```

This method will still detect and raise an exception when the controller responds with an error code.

## Logging
This library logs through the `logging` standard library, but adds a default null handler. If you'd like to see logs from this library, activate logging for the `asitiger` logger, which is the parent logger under which all loggers for this library live.

```python
import logging

logging.basicConfig()
logging.getLogger("asitiger").setLevel(logging.DEBUG)

tiger.where(["X", "Y"])
tiger.move_relative({"X": -10000, "Y": 10000})

# Log messages:
# DEBUG:asitiger.serialconnection:Sending data: b'W X Y\r'
# DEBUG:asitiger.serialconnection:Received: b':A -989110.5 -1042395.0 \r\n'
# DEBUG:asitiger.serialconnection:Sending data: b'R X=-10000 Y=10000\r'
# DEBUG:asitiger.serialconnection:Received: b':A \r\n'
```