import time
from modules import settings
from modules.logging import *

FONT_8x5 = None
FONT_5x3 = None


def set_pixel(x, y, color):
    """
    Set a pixel on the matrix. If the interface is "8x8big", combine four pixels into one.
    """
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        index = settings.CURRENT_ARRAY[y * WIDTH + x]
        settings.np[index] = color  # type: ignore


def is_message_supported(message, font):
    """
    Check if all characters in the message are supported by the provided font.

    :param message: The message to check (string).
    :param font: The font dictionary mapping characters to their pixel representation.
    :return: True if all characters are supported, False otherwise.
    """
    unsupported_chars = []

    for char in message:
        if char not in font:
            unsupported_chars.append(char)

    if unsupported_chars:
        for char in unsupported_chars:
            log_warning(f"Unsupported character found for scrolling text: '{char}'")
        return False

    return True


def clear_matrix():
    for i in range(settings.LED_COUNT):
        settings.np[i] = (0, 0, 0)  # type: ignore


def draw_char(x_offset, char, color):
    pattern = FONT.get(char, [0b00000] * (8 if FONT == FONT_8x5 else 5))  # Standard 8 lines  # type: ignore
    for y, row in enumerate(pattern):
        for x in range((5 if FONT == FONT_8x5 else 3)):  # 5 rows per char
            if row & (1 << ((4 if FONT == FONT_8x5 else 2) - x)):  # check if each bit is on
                set_pixel(x + x_offset, y + VERTICAL_OFFSET, color)


def scroll_text(message, speed=0.1, color=(0, 100, 120), iterations=1):
    log_info(f"Starting scolling text: {message}")
    if not message:
        log_error("An empty message was passed.")
        return False
    is_message_supported(message=message, font=FONT)

    runs = 0
    while runs < iterations:
        runs += 1
        for offset in range(WIDTH, -(len(message) * (6 if FONT == FONT_8x5 else 4)), -1):  # font width 5 + 1 spacing
            clear_matrix()
            for i, char in enumerate(message):
                draw_char(i * (6 if FONT == FONT_8x5 else 4) + offset, char, color)
            settings.np.write()
            time.sleep(speed)


def load_font(font_type):
    global FONT_5x3

    if font_type == "5x3":
        if FONT_5x3 is None:
            FONT_5x3 = {
                '0': [0b111, 0b101, 0b101, 0b101, 0b111],
                '1': [0b010, 0b110, 0b010, 0b010, 0b111],
                '2': [0b111, 0b001, 0b111, 0b100, 0b111],
                '3': [0b111, 0b001, 0b111, 0b001, 0b111],
                '4': [0b101, 0b101, 0b111, 0b001, 0b001],
                '5': [0b111, 0b100, 0b111, 0b001, 0b111],
                '6': [0b111, 0b100, 0b111, 0b101, 0b111],
                '7': [0b111, 0b001, 0b001, 0b001, 0b001],
                '8': [0b111, 0b101, 0b111, 0b101, 0b111],
                '9': [0b111, 0b101, 0b111, 0b001, 0b111],
                '.': [0b000, 0b000, 0b000, 0b000, 0b010],
                ':': [0b000, 0b000, 0b010, 0b000, 0b010],
                'I': [0b010, 0b010, 0b010, 0b010, 0b010],
                'P': [0b111, 0b101, 0b111, 0b100, 0b100],
                ' ': [0b000, 0b000, 0b000, 0b000, 0b000],
                'M': [0b101, 0b111, 0b101, 0b101, 0b101],
                'A': [0b010, 0b101, 0b111, 0b101, 0b101],
                'X': [0b101, 0b010, 0b010, 0b010, 0b101],
                'C': [0b011, 0b100, 0b100, 0b100, 0b011],
                'E': [0b111, 0b100, 0b111, 0b100, 0b111]
            }
        return FONT_5x3


# Usage
font_type = "5x3"
FONT = load_font(font_type)
WIDTH = int(settings.config.get("led.width", 8))
HEIGHT = int(settings.config.get("led.height", 8))
VERTICAL_OFFSET = (HEIGHT - 6) // 2  # Make text center (font height is 8)


log_info("Scrolling text module initialized.")
# scroll_text("1234567890", speed=0.1)
