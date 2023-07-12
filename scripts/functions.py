import os
import sys
import json

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DeltaValue:
    """Class that updates a value based on deltatime"""
    def __init__(
            self, duration: int, min_value: object, max_value: object,
            function: object=None
    ):
    
        # PROPERTIES
        self.sign = 1
        self.time = 0
        self.value = 0
        self.duration = duration
        self.min_value = min_value
        self.max_value = max_value
        self.function = function
    
    def update(self, dt: int) -> None:
        """Updates the value based on deltatime"""
        self.time += dt * self.sign

        # CHECK IF INCREMENT OR DECREMENT
        if self.time > self.duration:
            self.time = self.duration
            self.sign *= -1
        elif self.time < 0:
            self.time = 0
            self.sign *= -1
        
        # GET CURRENT VALUE
        t = self.time/self.duration
        dvalue = (self.max_value-self.min_value) * t
        self.value = self.min_value + dvalue

        # CALL THE FUNCTION IF ANY PROVIDED
        if self.function: self.function(self.value)
    
    def reset(self) -> None:
        """Resets the timer"""
        self.time = 0


class Config:
    """Manages the configuration file"""
    def __init__(self, path: str):

        # PROPERTIES
        self.path = f'{os.path.dirname(path)}/settings/config.json'
        self.path = resource_path(self.path)
        self.config = self.load()

    def get(self, key: str, default: object=None) -> object:
        """Returns the given value from the dictionary"""
        return self.config.get(key, default)

    def load(self) -> dict:
        """Loads the configuration"""
        with open(self.path, 'r') as f:
            config = json.load(f)
        return config

    def save(self) -> None:
        """Saves the configuration"""
        with open(self.path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def update(self, key: str, value: object) -> None:
        """Updates the configuration"""
        self.config[key] = value
        self.save()