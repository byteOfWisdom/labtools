from dataclasses import dataclass

settings = {
    'localization': None,
}

def set_setting(setting, value):
    global settings
    settings[setting] = value


def get_setting(key):
    return settings[key]