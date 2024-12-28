import uasyncio as asyncio
import modules.settings as settings
import gc
import network
from modules.led_controller import clear_leds
from modules.wifi import connect_wifi, set_time
from modules.logging import *
import modules.routing as routing


async def main():
    asyncio.create_task(settings.app.start_server(debug=True, port=80))
    asyncio.create_task(main_loop())
    while True:
        await asyncio.sleep(0.01)


async def main_loop():
    import main_loop
    await main_loop.start_main_loop()

clear_leds()
connect_wifi()
set_time()
gc.collect()
routing.register_routes()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    log_warning("Exiting...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    clear_leds()
    import machine
    # machine.reset()
except Exception as e:
    log_error(f"An error occured: {e}")
    import sys
    sys.print_exception(e)  # type: ignore
    log_exception_to_file(e)
    import machine
    machine.reset()
