# BussDCC Hardware

**bussdcc-hardware** provides hardware device integrations for `bussdcc`.

It includes drivers for common buses and devices and exposes them through the BussDCC device system so they can be managed, monitored, and orchestrated by the runtime.

# Architecture

Hardware in BussDCC is modeled as devices in a dependency graph. Bus devices are one common kind of dependency node.

```
Runtime
  ├── Bus Devices
  │     ├── I2C Bus
  │     ├── 1-Wire Bus
  │     └── GPIO Bus
  │
  └── Hardware Devices
        ├── Sensors
        ├── ADCs
        ├── Cameras
        └── Actuators
```

Each hardware component is represented as a **BussDCC Device** with a managed lifecycle:

```
connect → operate → disconnect
```

The runtime handles:

* device initialization
* dependency ordering
* failure detection
* online/offline status

# Features

## Bus Drivers

Hardware buses are modeled as devices themselves.

Currently supported:

### I²C

```
bussdcc_hardware.bus.i2c
```

Features:

* bus discovery
* device address scanning
* register bus interface

### 1-Wire

```
bussdcc_hardware.bus.w1
```

Features:

* device discovery
* filesystem-based device access

## Hardware Devices

### NAU7802 Load Cell ADC

High precision load cell amplifier.

```
bussdcc_hardware.device.nau7802
```

Features:

* dual channel support
* calibration parameters
* automatic channel switching
* failure detection

### DS18B20 Temperature Sensor

1-Wire temperature sensor.

```
bussdcc_hardware.device.ds18b20
```

Features:

* filesystem-based reading
* automatic offline detection

### USB Camera

OpenCV-based camera integration.

```
bussdcc_hardware.device.usb_camera
```

Features:

* configurable resolution and FPS
* exposure control
* focus control
* white balance control
* automatic failure recovery

### Digital Output

Simple GPIO-based actuator for controlling devices such as pumps, relays, LEDs, or lights.

```
bussdcc_hardware.device.digital_output
```

Features:

* on/off control
* safe shutdown

# Device Configuration

All devices use **typed dataclass configurations**.

Example:

```python
from bussdcc_hardware.device.nau7802 import NAU7802Config

config = NAU7802Config(
    bus_id="i2c0",
    addr=0x2A,
)
```

Configuration metadata includes UI hints:

* labels
* groups
* help text
* numeric constraints
* dependency references

This allows configuration systems or web interfaces to automatically generate forms.

Example metadata:

```
{
  "label": "Frame Width",
  "group": "Video",
  "min": 160,
  "max": 3840
}
```

# Device Discovery

Hardware integrations are registered using **Python entry points**.

```
bussdcc.device
```

The registry loads available devices automatically:

```python
from bussdcc_hardware.registry import registry

registry.devices
```

Unavailable drivers (missing optional dependencies) are detected and reported.

# Optional Dependencies

Some hardware drivers require additional libraries.

Install them using extras:

```
pip install bussdcc-hardware[nau7802]
pip install bussdcc-hardware[digital_output]
pip install bussdcc-hardware[usb_camera]
```

# Example

Example hardware configuration:

```python
runtime.add_device(
    "i2c0",
    "i2c",
    {
        "bus": 1
    }
)

runtime.add_device(
    "scale_adc",
    "nau7802",
    {
        "bus_id": "i2c0",
        "addr": 0x2A
    }
)
```

The runtime attaches devices in dependency order.

# Design Goals

### Hardware as first-class devices

Buses and sensors are modeled the same way as any other BussDCC device.

### Runtime-managed lifecycle

Devices automatically:

* connect
* report failures
* recover when possible

### Strong typing

All configurations are statically typed dataclasses.

### Composable integrations

Hardware modules can be distributed as independent packages and discovered through entry points.

# Installation

```
pip install bussdcc-hardware
```

Optional drivers:

```
pip install bussdcc-hardware[nau7802]
pip install bussdcc-hardware[digital_output]
pip install bussdcc-hardware[usb_camera]
```

# Related Projects

* **bussdcc** — cybernetic runtime kernel
* **bussdcc-framework** — runtime utilities and web interface

# License

MIT License
