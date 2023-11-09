"""
This module defines the abstract base class for handling authentication tokens.

It includes the definition of the Token class which encapsulates the properties and methods related to an authentication token, such as the token's value and its expiration details. The class provides functionality to convert token information to JSON, save it to a file, and check the token's validity.
"""
import configparser
import json
import os
import errno
from abc import ABC, abstractmethod
from datetime import datetime

class Token(ABC):
    """
    Abstract base class for a generic authentication token.

    Attributes:
        value (str): The value of the token.
        expiration_timestamp (float): The Unix timestamp when the token expires.

    Methods:
        value: Property to get or set the token's value.
        expiration_timestamp: Property to get or set the token's expiration timestamp.
        expires_at: Property to get the token's expiration as a datetime object.
        is_expired: Method to check if the token is expired.
        show_expire_date: Method to get the token's expiration date as a string.
        to_json: Method to serialize the token to a JSON-compliant dictionary.
        save_to_json: Method to save the token information as JSON to a file.
        to_config_ini: Abstract method to serialize the token for a .ini config.
        save_to_config_ini: Method to save the token information to a .ini file.
        is_valid: Abstract method to check the token's validity.
    """

    def __init__(self, value:str, expiration_timestamp:str):
        """
        Initialize a new Token instance.

        Args:
            value (str): The token value as a string.
            expiration_timestamp (str): The expiration time as a Unix timestamp string.
        """
        self.__value= value
        self.__expiration_timestamp = float(expiration_timestamp)

    @property
    def value(self) -> str:
        """
        Get the token's value.

        Returns:
            str: The current value of the token.
        """
        return self.__value

    @value.setter
    def value(self,value:str):
        """
        Set the token's value.

        Args:
            value (str): The new value to assign to the token.
        """
        self.__value = value

    @property
    def expiration_timestamp(self) -> float:
        """
        Get the token's expiration timestamp.

        Returns:
            float: The current expiration timestamp of the token.
        """
        return self.__expiration_timestamp

    @expiration_timestamp.setter
    def expiration_timestamp(self,expiration_timestamp:str):
        """
        Set the token's expiration timestamp.

        Args:
            expiration_timestamp (str): The new expiration timestamp to assign to the token.
        """
        self.__expiration_timestamp = float(expiration_timestamp)

    @property
    def expires_at(self) -> datetime:
        """
        Get the expiration time as a datetime object.

        Returns:
            datetime: The expiration time of the token.
        """
        return datetime.fromtimestamp(self.__expiration_timestamp)

    @property
    def is_expired(self) -> bool:
        """
        Check if the token is expired.

        Returns:
            bool: True if the current time is past the token's expiration, False otherwise.
        """
        return self.expires_at>datetime.now()

    def show_expire_date(self) -> str:
        """
        Get the token's expiration date as a formatted string.

        Returns:
            str: The expiration date in 'YYYY-MM-DD HH:MM:SS' format.
        """
        return self.expires_at.strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        """
        Serialize the token to a JSON-compliant dictionary.

        Returns:
            dict: The token's data serialized as a dictionary.
        """
        return {
            'value': self.value,
            'expiration_timestamp': self.expiration_timestamp,
            'expires_at': self.expires_at
        }

    def save_to_json(self, filepath:str):
        """
        Save the token information as a JSON file at the specified filepath.

        Args:
            filepath (str): The path where the JSON file will be saved.

        Raises:
            OSError: If an error occurs while creating directories.
            IOError: If an error occurs while writing the file.
            Exception: If an unexpected error occurs.
        """
        # Convert the Token object into a dictionary for JSON serialization
        token_data = self.to_json()

        # Check if the directory exists, if not create it
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # Attempt to write the dictionary to a JSON file
        try:
            with open(filepath, 'w') as json_file:
                json.dump(token_data, json_file, indent=4)
        except IOError as e:
            print(f"An error occurred while writing the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def to_config_ini(self):
        """
        Serialize the token for saving to a .ini configuration file.

        This is an abstract method that must be implemented by subclasses.
        """
        # This is an abstract method that must be implemented by child classes
        pass

    def save_to_config_ini(self, filepath):
        """
        Save the token information to a .ini configuration file at the specified filepath.

        Args:
            filepath (str): The path where the .ini file will be saved.

        Raises:
            IOError: If an error occurs while writing the file.
        """
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
        """
        Return an unambiguous string representation of the token.

        Returns:
            str: A string representation of the token showing its value and expiration date.
        """
        return f"Token(value='{self.value}', expires_at='{self.expires_at}')"

    def is_valid(self):
        """
        Check the validity of the token.

        This is an abstract method that must be implemented by subclasses to define what makes a token valid.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        # This is an abstract method that must be implemented by child classes
        pass
