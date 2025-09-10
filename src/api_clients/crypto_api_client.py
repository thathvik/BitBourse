from http import HTTPMethod
from requests import Response

from src.api_clients.base_api_client import BaseApiClient, ConvertableToFloat

from src.constants import (
    STR_FREE, STR_PREMIUM, COIN_GECKO_SUBSCRIPTION, COIN_GECKO_API_KEY,
    COIN_GECKO_DEMO_API_URL, COIN_GECKO_DEMO_API_KEY_HEADER,
    COIN_GECKO_PRO_API_URL, COIN_GECKO_PRO_API_KEY_HEADER,
    COIN_GECKO_SIMPLE_PRICE_ENDPOINT, STR_GET, STR_POST, STR_USD,
    COIN_GECKO_SIMPLE_SUPPORTED_CRYPTO_ENDPOINT
)

from src.logger import get_logger

logger = get_logger(__name__)


class CryptoApiClient(BaseApiClient):

    def __init__(self, base_url: str, api_key_header: str, api_key: str) -> None:
        super().__init__(base_url)
        self.headers    = {
            api_key_header: api_key
        }
        self.CURRENCY           = STR_USD
        self.supported_cryptos  = self.get_supported_crypto_symbol_list()


    @classmethod
    def from_subscription_type(cls, api_key: str = COIN_GECKO_API_KEY, subscription: str = COIN_GECKO_SUBSCRIPTION) -> "CryptoApiClient":
        subscription_api_mapping = {
            STR_FREE    : (COIN_GECKO_DEMO_API_URL, COIN_GECKO_DEMO_API_KEY_HEADER),
            STR_PREMIUM : (COIN_GECKO_PRO_API_URL, COIN_GECKO_PRO_API_KEY_HEADER)
        }

        if subscription in subscription_api_mapping.keys():
            base_url, api_key_header = subscription_api_mapping[subscription]
        else:
            msg = f"{cls.__name__}.from_subscription_type(): Invalid {subscription=}. Expected {subscription_api_mapping.keys()=}"
            logger.error(msg)
            raise ValueError(msg)
        
        return cls(base_url, api_key_header, api_key)
    

    def get_supported_crypto_symbol_list(self) -> list[str]:
        logger.debug(f"+get_supported_crypto_symbol_list()")
        
        endpoint = COIN_GECKO_SIMPLE_SUPPORTED_CRYPTO_ENDPOINT
        response = self.rest_call(http_method=HTTPMethod.GET, endpoint=endpoint)

        crypto_list = response.json()

        # Using Pythnoic approach to raise exception
        if not (isinstance(crypto_list, list) and all(isinstance(symbol, str) for symbol in crypto_list)):
            msg = f"get_supported_crypto_symbol_list(): Unexpected output. Expected 'list', recevied {type(crypto_list)=}. All values in list must be strings."
            logger.error(msg)
            raise ValueError(msg)

        logger.debug(f"-get_supported_crypto_symbol_list()")
        return crypto_list
    

    def validate_crypto_list(self, crypto_symbol: list) -> bool:
        logger.debug(f"+check_if_symbols_is_supported()")
        
        is_subset = set(crypto_symbol) <= set(self.supported_cryptos)

        logger.debug(f"-check_if_symbols_is_supported()")
        return is_subset


    def get_price(self, crypto_symbols: list) -> dict[str, float]:
        logger.debug(f"+get_price()")

        if self.validate_crypto_list(crypto_symbols):
            endpoint = COIN_GECKO_SIMPLE_PRICE_ENDPOINT
            params = {
                "vs_currencies" : self.CURRENCY,
                "symbols"       : ",".join(crypto_symbols)
            }

            response = self.rest_call(http_method=HTTPMethod.GET, endpoint=endpoint, params=params)
            crypto_prices = self._extract_price_from_response(crypto_symbols, response)
        
        else:
            msg = f"get_price(): Some or all of the crypto symbols in the list are not supported. Following is the list of all the supported Cryptos. {self.supported_cryptos=}"
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-get_price()")
        return crypto_prices

    
    def _extract_price_from_response(self, crypto_symbols: list, response: Response) -> dict[str, float]:
        logger.debug(f"+_extract_price_from_response()")
        
        response_json = response.json()
        prices = {}

        if isinstance(response_json, dict):
            for symbol in crypto_symbols:
                
                if symbol in response_json:
                    price_info = response_json[symbol]
                    
                    if isinstance(price_info, dict) and self.CURRENCY in price_info:
                        price = price_info[self.CURRENCY]

                        if isinstance(price, ConvertableToFloat):
                            prices[symbol] = float(price)

                        else:
                            msg = f"_extract_price_from_response(): {type(price)=} cannot be converted into a float."
                            logger.error(msg)
                            raise ValueError(msg)
                    
                    else:
                        msg = f"_extract_price_from_response(): Unexpected 'price_info', expected dict and '{self.CURRENCY}' to be a key. {type(price_info)=} {price_info=}"
                        logger.error(msg)
                        raise ValueError(msg)
                
                else:
                    msg = f"_extract_price_from_response(): '{symbol}' not present in the response_json. Recevied {response_json.keys()}"
                    logger.error(msg)
                    raise ValueError(msg)
        
        else:
            msg = f"_extract_price_from_response(): Expected 'response_json' to be 'dict', received {type(response_json)=}."
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-_extract_price_from_response()")
        return prices
    

if __name__ == "__main__":
    crypto_api_client = CryptoApiClient.from_subscription_type(COIN_GECKO_API_KEY, STR_FREE)
    prices = crypto_api_client.get_price(["eth", "btc", "ltc"])

    import json
    print(json.dumps(prices, indent=4))
