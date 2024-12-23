try:
    import utime as time
except ModuleNotFoundError:
    import time


def red_text(msg: str) -> str:
    """Returns text in red"""
    return ('\033[31m' + str(msg) + '\033[0m')


def yellow_text(msg: str) -> str:
    """Returns text in yellow"""
    return ('\033[33m' + str(msg) + '\033[0m')


def green_text(msg: str) -> str:
    """Returns text in green"""
    return ('\033[32m' + str(msg) + '\033[0m')


def colored_text(msg: str, rgb: tuple[int, int, int]) -> str:
    color_code = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    reset_code = "\033[0m"
    return (f"{color_code}{msg}{reset_code}")


def blue_text(msg: str) -> str:
    """Returns text in blue"""
    return ('\033[34m' + str(msg) + '\033[0m')


def pre_zero(value: int) -> str:
    """Add a 0 in front of numbers smaller than 10"""
    try:
        str_value = str(value)
        if value < 10:
            str_value = f'0{value}'
        return str_value
    except Exception:
        str_value = str(value)
        return str_value


def log_info(*args, **kwargs):
    msg = _prefix(1) + " ".join(map(str, args), **kwargs)
    print(msg)


def log_warning(*args, **kwargs):
    msg = _prefix(2) + " ".join(map(str, args), **kwargs)
    print(yellow_text(msg))


def log_error(*args, **kwargs):
    msg = _prefix(3) + " ".join(map(str, args), **kwargs)
    print(red_text(msg))
    _saveLog(msg)


def _prefix(type: int) -> str:
    now = time.localtime()
    timestamp = "{}.{}.{}".format(pre_zero(now[2]), pre_zero(now[1]), pre_zero(now[0])) + " " + "{}:{}:{}".format(pre_zero(now[3]), pre_zero(now[4]), pre_zero(now[5]))
    if type == 1:
        return timestamp + " [INFO] "
    elif type == 2:
        return timestamp + " [WARNING] "
    elif type == 3:
        return timestamp + " [ERROR] "
    else:
        return timestamp + " [INFO] "


def _saveLog(msg: str) -> bool:
    """Saves a message to log.log

    Args:
        msg (str): The message to save

    Returns:
        bool: True if successful
    """
    try:
        log_entry = f"{msg}\n"

        # Open the file in read mode, create if it doesn't exist
        with open("log.log", "a+") as file:
            file.seek(0)
            lines = file.readlines()

        # Reopen the file in write mode
        with open("log.log", "w") as file:
            # Write the last 29 lines back to the file
            for line in lines[-29:]:
                file.write(line)

            # Append the new log entry
            file.write(log_entry)
        return True
    except Exception as e:
        print("Failed writing to log file.", e)
        return False


log_info("Logging initialized.")