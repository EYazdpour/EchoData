import time
from typing import Any, Dict, Optional

import requests


def make_request(url: str, method: str = 'GET', headers: Optional[Dict[str, str]] = None,
                 data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, str]] = None,
                 timeout: int = 30) -> Dict[str, Any]:
    """
    Make an HTTP request to a specified URL.

    Args:
        url (str): The URL to which the request is to be made.
        method (str): The HTTP method, e.g., 'GET', 'POST', etc.
        headers (dict): Optional HTTP headers to send with the request.
        data (dict): Optional JSON data to send with the request.
        params (dict): Optional URL parameters to append to the URL.
        timeout (int): How many seconds to wait for the server to send data before giving up.

    Returns:
        A JSON response as a dictionary.
    """
    try:
        response = requests.request(method, url, headers=headers, json=data, params=params, timeout=timeout)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        print(f"An error occurred: {e}")
        raise
    else:
        return response.json()  # Parse JSON response and return it


def retry(max_retries=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            mdelay = delay
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"An error occurred: {e}. Retrying after {mdelay} seconds...")
                    time.sleep(mdelay)
                    mdelay *= 2  # Optional: Exponential backoff
            return None  # or you might want to re-raise the exception
        return wrapper
    return decorator
