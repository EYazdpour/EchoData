import configparser
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime


class Token(ABC):
    def __init__(self, value:str, expiration_timestamp:str):
        self.__value= value
        self.__expiration_timestamp = float(expiration_timestamp)

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self,value:str):
        self.__value = value

    @property
    def expiration_timestamp(self) -> float:
        return self.__expiration_timestamp

    @expiration_timestamp.setter
    def expiration_timestamp(self,expiration_timestamp:str):
        self.__expiration_timestamp = float(expiration_timestamp)

    @property
    def expires_at(self) -> datetime:
        return datetime.fromtimestamp(self.__expiration_timestamp)

    @property
    def is_expired(self) -> bool:
        return self.expires_at>datetime.now()

    def show_expire_date(self) -> str:
        return self.expires_at.strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return {
            'value': self.value,
            'expiration_timestamp': self.expiration_timestamp,
            'expires_at': self.expires_at
        }

    def save_to_json(self, filepath:str):
        # Convert the Token object into a dictionary for JSON serialization
        token_data = self.to_json()

        # Check if the directory exists, if not create it
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != os.errno.EEXIST:
                    raise

        # Attempt to write the dictionary to a JSON file
        try:
            with open(filepath, 'w') as json_file:
                json.dump(token_data, json_file, indent=4)
        except IOError as e:
            print(f"An error occurred while writing the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @abstractmethod
    def to_config_ini(self):
        # This is an abstract method that must be implemented by child classes
        pass

    def save_to_config_ini(self, filepath):
        config = self.to_config_ini()
        # Make sure to preserve existing data if the file already exists
        if os.path.exists(filepath):
            existing_config = configparser.ConfigParser()
            existing_config.read(filepath)
            # Merge the existing config with the new token data
            for section in config.sections():
                if section not in existing_config:
                    existing_config.add_section(section)
                for key, value in config[section].items():
                    existing_config[section][key] = value
            config = existing_config
        # Write the updated configuration to file
        with open(filepath, 'w') as configfile:
            config.write(configfile)

    def __repr__(self):
        return f"Token(value='{self.value}', expires_at='{self.expires_at}')"


    @abstractmethod
    def is_valid(self):
        # This is an abstract method that must be implemented by child classes
        pass

