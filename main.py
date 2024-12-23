import network
import modules.settings as settings
from uqmtt import MQTTClient
import machine
import binascii
import ssl
import json
from machine import Pin
from neopixel import NeoPixel
from modules.logging import *


def get_client_id():
    return binascii.hexlify(machine.unique_id())


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        log_info(f"Connecting to network {settings.config.get('wifi.ssid')}")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    log_info('Connected to Wifi, network config:', wlan.ifconfig())


def sub_cb(topic, msg):
    try:
        data = msg.decode("utf-8")
        data_dict = json.loads(data)
        progress = data_dict["print"]["mc_percent"]
        log_info(f"Current Progress: {progress}")

        # Write LEDs
        progress_leds = int(progress * LED_COUNT / 100)
        for i in range(LED_COUNT):
            if i < progress_leds:
                np[i] = (int(0 * LED_BRIGHTNESS), int(255 * LED_BRIGHTNESS), int(0 * LED_BRIGHTNESS))
            else:
                np[i] = (0, 0, 0)
        np.write()
    except Exception as e:
        log_error(f"Received message, but could not parse it: {e}")


log_info("Starting printer monitor, loading config...")

# Initialize variables
SSID = settings.config.get('wifi.ssid')
PASSWORD = settings.config.get('wifi.password')
PORT = settings.config.get('printer.port')
USER_PRINTER = settings.config.get('printer.user')
PASSWORD_PRINTER = settings.config.get('printer.password')
PRINTER_IP = settings.config.get('printer.ip')
TOPIC = f"device/{settings.config.get('printer.serial')}/report"
CLIENT_ID = get_client_id()

LED_BRIGHTNESS = settings.config.get('led.brightness')
LED_PIN = settings.config.get('led.pin')
LED_COUNT = int(settings.config.get('led.count'))

# LED initialization
np = NeoPixel(Pin(LED_PIN, Pin.OUT), LED_COUNT)


# Clear all LEDs (only needed for testing)
for i in range(LED_COUNT):
    np[i] = (0, 0, 0)
np.write()


# Set SSL contect (Micropython v1.23 minimum)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE
connect_wifi()

c = MQTTClient(CLIENT_ID,
               PRINTER_IP,
               PORT, 
               USER_PRINTER,
               PASSWORD_PRINTER,
               3600,
               ssl=context)
# Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
c.connect()
c.subscribe(TOPIC)
log_info(f"Connected to {blue_text(PRINTER_IP)}, subscribed to topic {blue_text(TOPIC)}")

try:
    while 1:
        c.wait_msg()
finally:
    c.disconnect()
    log_info("User disconnected.")
