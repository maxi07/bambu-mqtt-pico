from modules.logging import *
from modules import settings

SYMBOL_INTERNET = [([3, 4, 11, 12, 30, 37, 36, 35, 34, 25, 47, 54, 61, 60, 59, 58, 49, 40], (0, 120, 100))]
SYMBOL_CHECK = [([31, 22, 13, 20, 27, 34, 41, 48], (0, 255, 0))]
SYMBOL_ERROR_GENERAL = [([58, 59, 60, 61, 62, 54, 46, 38, 37, 36, 30, 22, 14, 6, 5, 4, 3, 2], (255, 0, 0))]
SYMBOL_PRINT_ERROR = [([63, 54, 45, 36, 27, 18, 9, 8, 56, 49, 42, 35, 28, 21, 14, 7], (255, 0, 0))]


def show_symbol(symbol: list, color: tuple = (0, 0, 0)):
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
