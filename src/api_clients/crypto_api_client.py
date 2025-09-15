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
    # Class variable to control symbol validation
    # Set to True to skip validation (useful when API endpoint is broken)
    # This is a good example of using class variables for configuration
    SKIP_SYMBOL_VALIDATION = True

    def __init__(self, base_url: str, api_key_header: str, api_key: str) -> None:
        super().__init__(base_url)
        self.headers    = {
            api_key_header: api_key
        }
        self.CURRENCY           = STR_USD

        # Only fetch supported cryptos if validation is enabled
        # This shows students how to use conditional logic based on configuration
        self.supported_cryptos = [] if self.SKIP_SYMBOL_VALIDATION else self.get_supported_crypto_symbol_list()



    @classmethod
    def from_subscription_type(cls, subscription: str = COIN_GECKO_SUBSCRIPTION) -> "CryptoApiClient":
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
        
        return cls(base_url, api_key_header, COIN_GECKO_API_KEY)
    

    def get_price(self, crypto_symbol: str) -> float:
        logger.debug(f"+get_price()")

        prices = self.get_prices([crypto_symbol])

        price  = prices[crypto_symbol]

        logger.debug(f"-get_price()")
        return price


    def get_prices(self, crypto_symbols: list) -> dict[str, float]:
        logger.debug(f"+get_prices()")

        # This demonstrates Python's short-circuit evaluation:
        # If SKIP_SYMBOL_VALIDATION is True, validate_crypto_list() is never called
        # This is efficient and shows students how to handle API limitations gracefully
        if self.SKIP_SYMBOL_VALIDATION or self.validate_crypto_list(crypto_symbols):
            # We can proceed: either validation is skipped OR symbols are valid
            endpoint = COIN_GECKO_SIMPLE_PRICE_ENDPOINT
            params = {
                "vs_currencies" : self.CURRENCY,
                "symbols"       : ",".join(crypto_symbols)
            }

            response = self.rest_call(http_method=HTTPMethod.GET, endpoint=endpoint, params=params)
            crypto_prices = self._extract_prices_from_response(crypto_symbols, response)
        
        else:
            msg = f"get_prices(): Some or all of the crypto symbols in the list are not supported. Following is the list of all the supported Cryptos. {self.supported_cryptos=}"
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-get_prices()")
        return crypto_prices

    
    def _extract_prices_from_response(self, crypto_symbols: list, response: Response) -> dict[str, float]:
        logger.debug(f"+_extract_prices_from_response()")
        
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
                            msg = f"_extract_prices_from_response(): {type(price)=} cannot be converted into a float."
                            logger.error(msg)
                            raise ValueError(msg)
                    
                    else:
                        msg = f"_extract_prices_from_response(): Unexpected 'price_info', expected dict and '{self.CURRENCY}' to be a key. {type(price_info)=} {price_info=}"
                        logger.error(msg)
                        raise ValueError(msg)
                
                else:
                    msg = f"_extract_prices_from_response(): '{symbol}' not present in the response_json. Recevied {response_json.keys()}"
                    logger.error(msg)
                    raise ValueError(msg)
        
        else:
            msg = f"_extract_prices_from_response(): Expected 'response_json' to be 'dict', received {type(response_json)=}."
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-_extract_prices_from_response()")
        return prices
    

    def get_supported_crypto_symbol_list(self) -> list[str]:
        """
        Fetches the list of supported cryptocurrency symbols from the API.

        NOTE: The CoinGecko API endpoint for supported currencies is currently broken.
        When SKIP_SYMBOL_VALIDATION is True, this method returns an empty list.

        This method is kept for future use when the API is fixed.
        It demonstrates good practice: keeping code that will be needed later,
        even if it's temporarily disabled.

        Returns:
            list: List of supported crypto symbols (empty if validation is skipped)
        """
        logger.debug(f"+get_supported_crypto_symbol_list()")

        crypto_list = []

        # Early return if validation is skipped
        # This is a good pattern for students to learn
        if not self.SKIP_SYMBOL_VALIDATION:
            endpoint = COIN_GECKO_SIMPLE_SUPPORTED_CRYPTO_ENDPOINT
            response = self.rest_call(http_method=HTTPMethod.GET, endpoint=endpoint)

            crypto_list = response.json()

            # Validate the response format
            # This shows students how to check data types before using them
            if not (isinstance(crypto_list, list) and all(isinstance(symbol, str) for symbol in crypto_list)):
                msg = f"get_supported_crypto_symbol_list(): Unexpected output. Expected 'list', recevied {type(crypto_list)=}. All values in list must be strings."
                logger.error(msg)
                raise ValueError(msg)
        else:
            logger.info("get_supported_crypto_symbol_list(): Symbol validation is disabled. Returning empty list.")

        logger.debug(f"-get_supported_crypto_symbol_list()")
        return crypto_list
    

    def validate_crypto_list(self, crypto_symbols: list) -> bool:
        """
        Validates if the given crypto symbols are supported.

        This method demonstrates the use of set operations in Python.
        It checks if all requested symbols are in the supported list.

        Args:
            crypto_symbol: List of cryptocurrency symbols to validate

        Returns:
            bool: True if all symbols are supported, False otherwise
        """
        logger.debug(f"+check_if_symbols_is_supported()")
        
        is_subset = set(crypto_symbols) <= set(self.supported_cryptos)

        logger.debug(f"-check_if_symbols_is_supported()")
        return is_subset
    

if __name__ == "__main__":
    crypto_api_client = CryptoApiClient.from_subscription_type(STR_FREE)
    list_symbols = crypto_api_client.get_supported_crypto_symbol_list()
    prices = crypto_api_client.get_prices(["eth", "btc", "ltc"])

    import json
    print(json.dumps(prices, indent=4))
    print(json.dumps(list_symbols, indent=4))
