from http import HTTPMethod
from requests import Response

from src.api_clients.base_api_client import BaseApiClient, ConvertableToFloat

from src.constants import (
    ALPHA_VANTAGE_API_URL, ALPHA_VANTAGE_API_KEY_PARAM, ALPHA_VANTAGE_API_KEY, ALPHA_VATAGE_API_QUERY_ENDPOINT,
    STR_TIME_SERIES_DAILY, TIME_SERIES_DAILY_KEY, CLOSE_KEY
)

from src.logger import get_logger

logger = get_logger(__name__)

class StocksApiClient(BaseApiClient):

    def __init__(self, base_url: str = ALPHA_VANTAGE_API_URL, api_key_param: str = ALPHA_VANTAGE_API_KEY_PARAM, api_key: str = ALPHA_VANTAGE_API_KEY) -> None:
        super().__init__(base_url)
        self.params = {
            api_key_param: api_key
        }


    @staticmethod
    def from_subscription_type(subscription: str) -> 'StocksApiClient':
        # Currently Stocks API returns the same API Client Configurations for FREE and PREMIUM.
        return StocksApiClient()


    def get_price(self, stock_symbol: str) -> float:
        logger.debug(f"+get_price()")

        endpoint = ALPHA_VATAGE_API_QUERY_ENDPOINT
        params = {
            "function"  : STR_TIME_SERIES_DAILY,
            "symbol"    : stock_symbol,
        }
        
        response = self.rest_call(http_method=HTTPMethod.GET, endpoint=endpoint, params=params)
        stock_price = self._extract_price_from_response(response)
        
        logger.debug(f"-get_price()")
        return stock_price


    def _extract_price_from_response(self, response: Response) -> float:
        logger.debug(f"+_extract_price_from_response()")
        response_json = response.json()
        price = None

        if isinstance(response_json, dict):
            
            if TIME_SERIES_DAILY_KEY in response_json:
                time_series_response = response_json[TIME_SERIES_DAILY_KEY]
                latest_date = max(time_series_response.keys())
                price_info = time_series_response[latest_date]

                if CLOSE_KEY in price_info:
                    price = price_info[CLOSE_KEY]

                    if isinstance(price, ConvertableToFloat):
                        price = float(price)

                    else:
                        msg = f"_extract_price_from_response(): {type(price)=} cannot be converted into a float."
                        logger.error(msg)
                        raise ValueError(msg)
                else:
                    msg = f"_extract_price_from_response(): Unexpected 'price_info', expected dict and '{CLOSE_KEY}' to be a key. {type(price_info)=} {price_info=}"
                    logger.error(msg)
                    raise ValueError(msg)
            
            else:
                msg = f"_extract_price_from_response(): '{TIME_SERIES_DAILY_KEY}' not present in the response_json. Recevied {response_json.keys()}"
                logger.error(msg)
                raise ValueError(msg)
        
        else:
            msg = f"_extract_price_from_response(): Expected 'response_json' to be 'dict', received {type(response_json)=}."
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-_extract_price_from_response()")
        return price
    

if __name__ == "__main__":
    stocks_api_client = StocksApiClient()
    price = stocks_api_client.get_price("AAPL")

    print(price)