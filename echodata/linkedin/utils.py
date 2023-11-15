from typing import Any, Dict, Optional

from ..common.utils import make_request, retry


@retry(max_retries=3, delay=2, exceptions=(TimeoutError, ConnectionError))
def linkedin_get_request(endpoint: str, access_token: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """
    Send a GET request to the LinkedIn API.

    Args:
        endpoint (str): The API endpoint to be appended to the base URL.
        access_token (str): The OAuth access token for LinkedIn API authentication.
        params (Dict[str, Any], optional): URL parameters to append to the request.

    Returns:
        Any: The parsed JSON response from the LinkedIn API.

    Raises:
        TimeoutError, ConnectionError: For network-related issues, handled with retries.
        HTTPError: For unsuccessful HTTP responses.
    """
    base_url = 'https://api.linkedin.com/rest'
    url = f'{base_url}{endpoint}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Linkedin-Version': '202305',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    return make_request(url=url, method='GET', headers=headers, params=params)


def linkedin_paginated_request(endpoint: str, access_token: str, params: dict, max_count: int = 1000) -> List[Any]:
    """
    Make paginated GET requests to the LinkedIn API.

    Args:
        base_url (str): The base URL for the LinkedIn API endpoint.
        access_token (str): The OAuth access token for LinkedIn API authentication.
        params (dict): Initial URL parameters for the request.
        max_count (int): Maximum number of items to retrieve per request.

    Returns:
        List[Any]: A list of all items retrieved from the paginated API responses.
    """
    start = 0
    elements = []

    while True:
        params['start'] = start
        params['count'] = max_count
        response = linkedin_get_request(endpoint, access_token, params=params)
        data = response.json()
        elements.extend(data.get("elements", []))

        paging = data.get("paging", {})
        total = paging.get("total", 0)
        start += max_count

        if start >= total:
            break

    return elements
