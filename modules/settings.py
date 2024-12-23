from modules.logging import *
try:
    import ujson as json
except ImportError:
    import json


class Config:
    def __init__(self, config_file):
        self._config_file = config_file
        try:
            with open(config_file) as f:
                self._config = json.load(f)
                log_info("Reading config.")
        except Exception as ex:
            log_error("Failed reading config.", ex)

    def __iter__(self):
        return iter(self._config.items())

    def __len__(self):
        return len(self._config)

    def get(self, key: str, default=None):
        try:
            keys = key.split('.')
            value = self._config
            for k in keys:
                value = value.get(k, {})
            # log_info(f"Read config key {key} with value {value} of type {type(value)}")
            return value if value is not None else default
        except Exception as ex:
            log_error("Failed reading config.", ex)
            return default

    def set(self, key, value):
        '''
        Currently unused
        '''
        try:
            keys = key.split('.')
            curr_dict = self._config
            for k in keys[:-1]:
                curr_dict = curr_dict.setdefault(k, {})
            curr_dict[keys[-1]] = value
            with open(self._config_file, 'w') as f:
                json.dump(self._config, f)
        except Exception as ex:
            log_error(f"Failed saving {key} setting to config.", ex)


config = Config('config.json')
"""The config to get and set values from/to"""
