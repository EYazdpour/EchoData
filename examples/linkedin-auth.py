from echodata.linkedin.auth import generate_auth_url, exchange_code_for_token
import configparser
import os

# Get the directory in which the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the config.ini file
config_path = os.path.join(script_directory, "config.ini")

# Initialize the config parser and read the config file
config = configparser.ConfigParser()
config.read(config_path)

def main():
    client_id = config['LinkedIn Credentials']['CLIENT_ID']
    client_secret = config['LinkedIn Credentials']['CLIENT_SECRET']
    redirect_uri = config['LinkedIn Credentials']['REDIRECT_URI']

    # Step 1: Get the user to visit this URL and authenticate
    auth_url = generate_auth_url(client_id=client_id, redirect_uri=redirect_uri)
    print(f"Please visit this URL and authenticate:\n{auth_url}")

    # Step 2: Wait for the user to enter the authorization code
    auth_code = input("Please enter the authorization code you received: ")

    # Step 3: Exchange the code for a token & save it in the config.ini file
    LI_token = exchange_code_for_token(client_id=client_id, client_secret=client_secret, auth_code=auth_code, redirect_uri=redirect_uri)
    print(f"Access Token: {LI_token}")
    LI_token.save_to_config_ini(config_path)

# Check if we are running as a script, not imported as a module
if __name__ == "__main__":
    main()
