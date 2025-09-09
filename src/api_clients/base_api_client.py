import requests

from typing import Optional, Any, Union, SupportsFloat
from requests import Response
from urllib.parse import urljoin

from src.constants import STR_GET, STR_POST, LIST_SUPPORTED_HTTPS_METHODS

from src.logger import get_logger

logger = get_logger(__name__)

ConvertableToFloat = Union[int, str, float, SupportsFloat]


class BaseApiClient:

    def __init__(self, base_url: str) -> None:
        self.base_url   = base_url
        # Default (uniform for all calls)
        self.headers    = {}
        self.params     = {}
    

    def rest_call(self, http_method: str, endpoint: Optional[str] = None, headers: Optional[dict]= None, params: Optional[dict]= None, payload: Optional[Any]= None):
        logger.debug(f"+rest_call()")
        assert isinstance(http_method, str) and len(http_method) > 0, f"rest_call(): Invalid {type(http_method)=}"

        url = urljoin(self.base_url, endpoint)
        
        headers = self.headers if headers is None else self.headers | headers
        params  = self.params if params is None else self.params | params

        if http_method in LIST_SUPPORTED_HTTPS_METHODS:
            response = self.get(url, params, headers) if http_method == STR_GET else self.post(url, params, headers, payload)
        else:
            msg = f"rest_call(): {http_method=} is not one of the expected values '{LIST_SUPPORTED_HTTPS_METHODS}'"
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-rest_call()")
        return response


    def get(self, url: str, params: dict, headers: dict) -> Response:
        return requests.get(url=url, params=params, headers=headers)
    

    def post(self, url: str, params: dict, headers: dict, payload: Any) -> Response:
        return requests.post(url=url, params=params, headers=headers, data=payload)
    