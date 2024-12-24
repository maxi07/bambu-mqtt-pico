from modules.logging import *
from modules import settings

SYMBOL_INTERNET = [([3, 4, 11, 12, 30, 37, 36, 35, 34, 25, 47, 54, 61, 60, 59, 58, 49, 40], (0, 120, 100))]
SYMBOL_CHECK = [([31, 22, 13, 20, 27, 34, 41, 48], (0, 255, 0))]
SYMBOL_ERROR_GENERAL = [([58, 59, 60, 61, 62, 54, 46, 38, 37, 36, 30, 22, 14, 6, 5, 4, 3, 2], (255, 0, 0))]
SYMBOL_PRINT_ERROR = [([63, 54, 45, 36, 27, 18, 9, 8, 56, 49, 42, 35, 28, 21, 14, 7], (255, 0, 0))]
SYMBOL_PREPARE = [0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8]


def show_symbol(symbol: list, color: tuple = (0, 0, 0)):
    # Clear first
    for i in range(settings.LED_COUNT):
        settings.np[i] = (0, 0, 0)

    # Check for valid color
    for value in color:
        if value > 255 or value < 0:
            log_warning("Wrong color was given, using default.")
            color = (255, 255, 255)
            break

    for pixel_indices, rgb_color in symbol:
        if color == (0, 0, 0):
            r, g, b = rgb_color
        else:
            r, g, b = color
        for pixel_index in pixel_indices:
            settings.np[pixel_index] = (r, g, b)

    settings.np.write()


def next_item_from_list(items):
    """
    Generator, der nacheinander die Items aus einer Liste zurückgibt
    und am Ende wieder von vorne anfängt.
    """
    while True:
        for item in items:
            yield item


def update_prepare_symbol():
    """When print stage is eq 1, we show the prepare symbol"""
    global symbol_generator
    symbol = next(symbol_generator)

    # Clear first
    for i in range(settings.LED_COUNT):
        settings.np[i] = (0, 0, 0)

    settings.np[symbol] = settings.BLUE
    settings.np.write()


# Initialisiere den Generator
symbol_generator = next_item_from_list(SYMBOL_PREPARE)
