import network
import modules.settings as settings
from modules.logging import *
import modules.symbols as symbols
from modules.led_controller import clear_leds


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        log_info(f"Connecting to network {settings.config.get('wifi.ssid', 'unknownSSID')}")
        wlan.connect(settings.config.get('wifi.ssid', 'unknownSSID'), settings.config.get('wifi.password', 'unknownPassword'))
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
        import sys
        sys.exit()
        return
    else:
        clear_leds()
        symbols.show_symbol(symbols.SYMBOL_INTERNET, settings.GREEN)
        log_info('Connected to Wifi, network config:', wlan.ifconfig())
