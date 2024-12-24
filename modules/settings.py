from modules.logging import *
from machine import Pin
import machine
import binascii
from neopixel import NeoPixel
try:
    import ujson as json
except ImportError:
    import json


class Config:
    def __init__(self, config_file):
        self._config_file = config_file
        try:
            with open(config_file) as f:
                self._config = json.load(f)
                log_info("Reading config.")
        except Exception as ex:
            log_error("Failed reading config.", ex)

    def __iter__(self):
        return iter(self._config.items())

    def __len__(self):
        return len(self._config)

    def get(self, key: str, default=None):
        try:
            keys = key.split('.')
            value = self._config
            for k in keys:
                value = value.get(k, {})
            # log_info(f"Read config key {key} with value {value} of type {type(value)}")
            return value or default
        except Exception as ex:
            log_error("Failed reading config.", ex)
            return default

    def set(self, key, value):
        '''
        Currently unused
        '''
        try:
            keys = key.split('.')
            curr_dict = self._config
            for k in keys[:-1]:
                curr_dict = curr_dict.setdefault(k, {})
            curr_dict[keys[-1]] = value
            with open(self._config_file, 'w') as f:
                json.dump(self._config, f)
        except Exception as ex:
            log_error(f"Failed saving {key} setting to config.", ex)


def get_client_id():
    return binascii.hexlify(machine.unique_id())


config = Config('config.json')
"""The config to get and set values from/to"""

LED_PIN = config.get('led.pin')
LED_COUNT = int(config.get('led.count'))

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize variables
SSID = str(config.get('wifi.ssid'))
PASSWORD = str(config.get('wifi.password'))
PORT = int(config.get('printer.port'))
USER_PRINTER = str(config.get('printer.user'))
PASSWORD_PRINTER = str(config.get('printer.password'))
PRINTER_IP = str(config.get('printer.ip'))
TOPIC = f"device/{config.get('printer.serial')}/report"
CLIENT_ID = get_client_id()
LED_BRIGHTNESS = float(config.get('led.brightness'))

# LED initialization
np = NeoPixel(Pin(LED_PIN, Pin.OUT), LED_COUNT)
