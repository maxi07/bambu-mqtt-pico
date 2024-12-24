import network
import modules.settings as settings
from modules.uqmtt import MQTTClient
import ssl
import json
from modules import symbols
from modules.logging import *
import utime as time
from modules.buzzer import BuzzerMelody


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
        import sys
        sys.exit()
        return
    else:
        clear_leds()
        symbols.show_symbol(symbols.SYMBOL_INTERNET, settings.GREEN)
        log_info('Connected to Wifi, network config:', wlan.ifconfig())


def sub_cb(topic, msg):
    global last_progress
    try:
        data = msg.decode("utf-8")
        data_dict = json.loads(data)
        progress = int(data_dict["print"]["mc_percent"])
        error_code = int(data_dict["print"]["mc_print_error_code"])
        print_stage = int(data_dict["print"]["mc_print_stage"])
        upload_status = data_dict["print"]["upload"]["status"]
        gcode = data_dict["print"]["gcode_state"]
        log_info(f"Progress: {progress} | Error code: {error_code} | Print stage: {print_stage} | Upload status: {upload_status} | GCode: {gcode}")
        # Check for print error code
        if error_code != 0 or gcode.lower() == "FAILED".lower():
            log_error(f"Print error code: {error_code}")
            symbols.show_symbol(symbols.SYMBOL_PRINT_ERROR)
            return

        # Check for print stage, 1 means preparing, 2 means printing
        if print_stage == 1:
            symbols.update_prepare_symbol()
            return

        # If the progress is 100, show a checkmark
        if progress == 100:
            if last_progress == 99:
                last_progress = 100
                log_info("Print finished, playing buzzer melody.")
                player = BuzzerMelody()
                player._playsong("cantinaband")
            clear_leds(False)
            symbols.show_symbol(symbols.SYMBOL_CHECK)
            return
        else:
            last_progress = progress

        clear_leds(False)
        progress_leds = max(int(progress * settings.LED_COUNT / 100), 1)
        for i in range(settings.LED_COUNT):
            if i < progress_leds:
                settings.np[i] = (int(0 * settings.LED_BRIGHTNESS), int(255 * settings.LED_BRIGHTNESS), int(0 * settings.LED_BRIGHTNESS))
            else:
                settings.np[i] = (0, 0, 0)
        settings.np.write()
    except ValueError:
        log_warning("MEssage could not be decoded.")
        # log_warning(f"Message: {msg}")
    except KeyError as keyex:
        log_warning(f"Unsupported message, expected key not found: {keyex}")
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
# Set SSL contect (Micropython v1.23 minimum)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE
connect_wifi()
log_info("Starting MQTT client...")


c = MQTTClient(settings.CLIENT_ID,
               settings.PRINTER_IP,
               settings.PORT,
               settings.USER_PRINTER,
               settings.PASSWORD_PRINTER,
               3600,
               ssl=context)
# Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
try:
    c.connect(timeout=20)
except MQTTException as mqttex:
    log_error(f"Could not connect to MQTT protocoll, wrong password? Code {mqttex}")
except Exception as e:
    log_error(f"Could not connect to MQTT protocoll: {e}")
    import machine
    machine.reset()
c.subscribe(settings.TOPIC)
log_info(f"Connected to {blue_text(settings.PRINTER_IP)}, subscribed to topic {blue_text(settings.TOPIC)}")
last_progress = 0


try:
    while 1:
        c.wait_msg()
except Exception as e:
    log_error(f"An error occurred: {e}")
    import sys
    sys.print_exception(e)
    symbols.show_symbol(symbols.SYMBOL_ERROR_GENERAL)
except KeyboardInterrupt:
    log_warning("Keyboard interrupt, disconnecting...")
    clear_leds()
finally:
    c.disconnect()
    log_info("Disconnected.")
    import machine
    machine.reset()
