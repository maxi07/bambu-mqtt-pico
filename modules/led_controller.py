import modules.settings as settings


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
