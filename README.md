# Bambu MQTT Progress Display
This program prints the current printer progress on a 8x8 LED matrix, connected to a Raspberry Pico with Micropython v1.23.
This program has been tested for [Bambu Lab X1C Printer](https://eu.store.bambulab.com/products/x1-carbon?srsltid=AfmBOopFs9a93pwfv7qHibLEP5UfgySgJ1MaMIiTjB-XtYBMTHl01if_) that supports the MQTT protocoll.

![Bambu Labs X1C](/doc/X1C.png)

## Supported features
- [x] Print current progress 🟩
- [x] Show printer error ❌
- [x] Show preparation progress 🟦

## Setup
Please edit the `config.json` file and add your details.