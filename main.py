import network
import modules.settings as settings
from modules.uqmtt import MQTTClient
import ssl
import json
from modules import symbols
from modules.logging import *
import utime as time
import sys


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        log_info(f"Connecting to network {settings.SSID}")
        wlan.connect(settings.SSID, settings.PASSWORD)
        for i in range(40):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            if i % 2 == 0:
                clear_leds()
            else:
                symbols.show_symbol(symbols.SYMBOL_INTERNET, settings.YELLOW)
            print('.', end="")
            time.sleep(0.25)
        print(".")
    if not wlan.isconnected():
        log_error("Could not connect to Wifi.")
        clear_leds()
        symbols.show_symbol(symbols.SYMBOL_INTERNET, settings.RED)
        sys.exit()
        return
    else:
        clear_leds()
        symbols.show_symbol(symbols.SYMBOL_INTERNET, settings.GREEN)
        log_info('Connected to Wifi, network config:', wlan.ifconfig())


def sub_cb(topic, msg):
    try:
        data = msg.decode("utf-8")
        data_dict = json.loads(data)
        progress = data_dict["print"]["mc_percent"]
        error_code = int(data_dict["print"]["mc_print_error_code"])
        log_info(f"Current Progress: {progress}")

        # Check for print error code
        if error_code != 0:
            log_error(f"Print error code: {error_code}")
            symbols.show_symbol(symbols.SYMBOL_PRINT_ERROR)
            return

        # If the progress is 100, show a checkmark
        if progress == 100:
            clear_leds(False)
            symbols.show_symbol(symbols.SYMBOL_CHECK)
            return

        clear_leds(False)
        progress_leds = int(progress * settings.LED_COUNT / 100)
        for i in range(settings.LED_COUNT):
            if i < progress_leds:
                settings.np[i] = (int(0 * settings.LED_BRIGHTNESS), int(255 * settings.LED_BRIGHTNESS), int(0 * settings.LED_BRIGHTNESS))
            else:
                settings.np[i] = (0, 0, 0)
        settings.np.write()
    except Exception as e:
        log_error(f"Received message, but could not parse it: {e}")
        log_error(f"Message: {msg}")


def clear_leds(write: bool = True):
    """Clears all LEDS

    Args:
        write (bool, optional): Should only be set to false if you np.write after calling the function manually.
        Defaults to True.
    """
    for i in range(settings.LED_COUNT):
        settings.np[i] = (0, 0, 0)

    if write:
        settings.np.write()


clear_leds()
log_info("Starting MQTT client...")

# Set SSL contect (Micropython v1.23 minimum)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE
connect_wifi()

c = MQTTClient(settings.CLIENT_ID,
               settings.PRINTER_IP,
               settings.PORT,
               settings.USER_PRINTER,
               settings.PASSWORD_PRINTER,
               3600,
               ssl=context)
# Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
c.connect()
c.subscribe(settings.TOPIC)
log_info(f"Connected to {blue_text(settings.PRINTER_IP)}, subscribed to topic {blue_text(settings.TOPIC)}")

try:
    while 1:
        c.wait_msg()
except Exception as e:
    log_error(f"An error occurred: {e}")
    symbols.show_symbol(symbols.SYMBOL_ERROR_GENERAL)
except KeyboardInterrupt:
    log_warning("Keyboard interrupt, disconnecting...")
    clear_leds()
finally:
    c.disconnect()
    log_info("User disconnected.")
