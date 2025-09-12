import requests

from http import HTTPMethod
from typing import Optional, Any, Union, SupportsFloat
from urllib.parse import urljoin

from requests import Response

from src.logger import get_logger

logger = get_logger(__name__)

ConvertableToFloat = Union[int, str, float, SupportsFloat]


class BaseApiClient:

    def __init__(self, base_url: str) -> None:
        self.base_url   = base_url
        # Default (uniform for all calls)
        self.headers    = {}
        self.params     = {}
        self.LIST_SUPPORTED_HTTP_METHODS = [HTTPMethod.GET, HTTPMethod.POST]
    

    def rest_call(self, http_method: HTTPMethod, endpoint: Optional[str] = None, headers: Optional[dict]= None, params: Optional[dict]= None, payload: Optional[Any]= None):
        logger.debug(f"+rest_call()")
        assert isinstance(http_method, HTTPMethod), f"rest_call(): Invalid {type(http_method)=}, excepted 'HTTPMethod'"

        url = urljoin(self.base_url, endpoint)
        
        headers = self.headers if headers is None else self.headers | headers
        params  = self.params if params is None else self.params | params

        # Here, let's use a pythonic way of returning an exception.
        if http_method not in self.LIST_SUPPORTED_HTTP_METHODS:
            msg = f"rest_call(): {http_method=} is not one of the expected values '{self.LIST_SUPPORTED_HTTP_METHODS}'"
            logger.error(msg)
            raise ValueError(msg)
        
        response = self.get(url, params, headers) if http_method == HTTPMethod.GET else self.post(url, params, headers, payload)
        if not response.ok:
            msg = f"rest_call(): API returned with a status code '{response.status_code}':'{response.reason}'."
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-rest_call()")
        return response


    def get(self, url: str, params: dict, headers: dict) -> Response:
        return requests.get(url=url, params=params, headers=headers)
    

    def post(self, url: str, params: dict, headers: dict, payload: Any) -> Response:
        return requests.post(url=url, params=params, headers=headers, data=payload)
    