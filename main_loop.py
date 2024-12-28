import modules.settings as settings
from modules.uqmtt import MQTTClient
from modules.uqmtt import MQTTException
import ssl
import json
from modules import symbols
from modules.logging import *
from modules.buzzer import BuzzerMelody
from modules.led_controller import clear_leds
import uasyncio as asyncio


def sub_cb(topic, msg):
    global played_buzzer
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
        if error_code != 0 or gcode == "FAILED":
            # log_info(f"Print error code: {error_code}")
            symbols.show_symbol(symbols.SYMBOL_PRINT_ERROR)
            return

        if gcode == "FINISH":
            # log_info("Print finished.")
            if played_buzzer is False:
                player = BuzzerMelody()
                player._playsong("cantinaband")
                played_buzzer = True
            symbols.update_check_symbol()
            return

        if gcode == "PAUSE":
            # log_info("Print paused.")
            symbols.show_symbol(symbols.SYMBOL_PAUSE)
            return

        # Check for print stage, 1 means preparing, 2 means printing
        if gcode == "PREPARE":
            # log_info("Print stage is 1, showing prepare symbol.")
            symbols.update_prepare_symbol()
            return

        clear_leds(False)
        played_buzzer = False
        progress_leds = max(int(progress * settings.LED_COUNT / 100), 1)
        led_brightness = float(settings.config.get('led.brightness', 0.5))
        for i in range(settings.LED_COUNT):
            if i < progress_leds:
                settings.np[i] = (int(0 * led_brightness), int(255 * led_brightness), int(0 * led_brightness))
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


async def start_main_loop():
    await main_loop()


async def main_loop():
    # Set SSL contect (Micropython v1.23 minimum)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    log_info("Starting MQTT client...")
    connected: bool = False

    while not connected:
        try:
            c = MQTTClient(settings.CLIENT_ID,
                           settings.config.get('printer.ip', None),
                           settings.config.get('printer.port', 8883),
                           settings.config.get('printer.user', 'bblp'),
                           settings.config.get('printer.password', ''),
                           3600,
                           ssl=context)
            # Subscribed messages will be delivered to this callback
            c.set_callback(sub_cb)
            c.connect(timeout=20)
            connected = True
        except MQTTException as e:
            log_error(f"Could not connect to MQTT protocoll, wrong password? {e}")
            symbols.show_symbol(symbols.SYMBOL_LOCKED)
        except Exception as e:
            log_error(f"Could not connect to MQTT protocoll: {e}")
            import sys
            sys.print_exception(e)  # type:ignore
        await asyncio.sleep(5)
    topic = f"device/{settings.config.get('printer.serial', 'unknown ip')}/report"
    c.subscribe(topic)
    log_info(f"Connected to {blue_text(settings.config.get('printer.ip', 'unknown ip'))}, subscribed to topic {blue_text(topic)}")

    try:
        while 1:
            c.wait_msg()
            await asyncio.sleep(0.1)
    except Exception as e:
        log_error(f"An error occurred: {e}")
        import sys
        sys.print_exception(e)  # type:ignore
        log_exception_to_file(e)
        symbols.show_symbol(symbols.SYMBOL_ERROR_GENERAL)
        time.sleep(5)
        import machine
        machine.reset()

played_buzzer: bool = True
