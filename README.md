# Bambu MQTT Progress Display
This program prints the current printer progress on a 8x8 LED matrix, connected to a Raspberry Pico with [Micropython v1.23.](https://docs.micropython.org/en/v1.23.0/)
This program has been tested for [Bambu Lab X1C Printer](https://eu.store.bambulab.com/products/x1-carbon?srsltid=AfmBOopFs9a93pwfv7qHibLEP5UfgySgJ1MaMIiTjB-XtYBMTHl01if_) that supports the [MQTT](https://en.wikipedia.org/wiki/MQTT) protocoll. The printer pushes messages by standard every second, see example output [here](/doc/example_response.json). It requires a [Neopixel LED matrix](https://www.adafruit.com/product/1487) and a buzzer, see tutorial [here](https://www.tomshardware.com/how-to/buzzer-music-raspberry-pi-pico).

![Bambu Labs X1C](/doc/main.jpeg)

## Supported features
- [x] Print current progress 🟩
- [x] Show printer error ❌
- [x] Show preparation progress 🟦
- [x] Play buzzer sound if finished
- [x] Change printer access code via webinterface

## Setup
Please edit the `config.json` file and add your details:
- SSID
- SSID password
- Printer IP
- Printer password (Settings -> General)
- Printer serial (Settings -> General)

> [!IMPORTANT]  
> The printer password resets automatically after restarting the printer. You can change the password by opening the picos webinterface on its ip-address (port 80)

Other optioanl features, such as brightness can be configured via the `config.json` file.

> [!NOTE]  
> Only LAN mode can be either turned on or off and is not necessary.