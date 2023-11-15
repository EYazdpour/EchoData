import time
from typing import Any, Callable, Dict, Optional, TypeVar

import requests


def make_request(url: str, method: str = 'GET', headers: Optional[Dict[str, str]] = None,
                 data: Optional[Any] = None, params: Optional[Dict[str, str]] = None,
                 timeout: int = 30) -> requests.Response:
    """
    Make an HTTP request to a specified URL and return the raw response.

    Args:
        url (str): The URL to which the request is to be made.
        method (str): The HTTP method, e.g., 'GET', 'POST', etc.
        headers (Dict[str, str], optional): HTTP headers to send with the request.
        data (Any, optional): Data to send with the request. Could be dict, bytes, or file-like object.
        params (Dict[str, str], optional): URL parameters to append to the URL.
        timeout (int): Timeout for the request in seconds.

    Returns:
        requests.Response: The response object.

    Raises:
        requests.RequestException: For any issues with the request.
    """
    try:
        response = requests.request(method, url, headers=headers, data=data, params=params, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        print(f"An error occurred: {e}")
        raise


T = TypeVar('T')  # Generic type for decorator


def retry(max_retries: int = 3, delay: int = 1, exceptions: tuple = (Exception,)) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    A decorator that retries a function call upon specified exceptions.

    Args:
        max_retries (int): Maximum number of retries.
        delay (int): Delay between retries in seconds.
        exceptions (tuple): Exceptions to catch and retry on.

    Returns:
        Callable: Decorated function that will retry upon specified exceptions.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs) -> T:
            mdelay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Retry {attempt + 1}/{max_retries} for function {func.__name__} failed with error: {e}.")
                    if attempt + 1 < max_retries:
                        print(f"Retrying in {mdelay} seconds...")
                        time.sleep(mdelay)
                        mdelay *= 2  # Exponential backoff
            raise  # Re-raise the last exception if all retries failed
        return wrapper
    return decorator
