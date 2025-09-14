from typing import Union
from simple_term_menu import TerminalMenu

from src.api_clients.stocks_api_client import StocksApiClient
from src.api_clients.crypto_api_client import CryptoApiClient
from src.api_clients.api_client_factory import ApiClientFactory

from src.constants import STR_STOCKS, STR_CRYPTO, STR_FREE, STR_PREMIUM, STR_DEFAULT

from src.logger import get_logger

logger = get_logger(__name__)


class IOInterface:
    def __init__(self) -> None:
        pass


    def pick_api_client(self) -> Union[StocksApiClient, CryptoApiClient]:
        logger.debug(f"+pick_api_client()")

        market_map = {
            STR_STOCKS: self.get_stocks_api,
            STR_CRYPTO: self.get_crypto_api
        }
        print("Pick one of the following to find out some of the prices: ")
        options = list(market_map.keys())
        choice = self.default_menu(options)

        function = market_map[choice]
        api_client = function()

        logger.debug(f"-pick_api_client()")
        return api_client
    

    def get_stocks_api(self) -> StocksApiClient:
        logger.debug(f"+get_stocks_api()")
        api_client = self.call_api_factory(STR_STOCKS, STR_DEFAULT)
        
        if not isinstance(api_client, StocksApiClient):
            msg = f"get_stocks_api(): Unexpceted 'api_client' returned. Expected 'StocksApiClient', received {type(api_client)=}"
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-get_stocks_api()")
        return api_client
    

    def get_crypto_api(self) -> CryptoApiClient:
        logger.debug(f"+get_crypto_api()")
        options = [STR_FREE, STR_PREMIUM]
        option = self.default_menu(options)
        api_client = self.call_api_factory(STR_CRYPTO, option)
        
        if not isinstance(api_client, CryptoApiClient):
            msg = f"get_crypto_api(): Unexpceted 'api_client' returned. Expected 'CryptoApiClient', received {type(api_client)=}"
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-get_crypto_api()")
        return api_client
    

    def call_api_factory(self, market: str, subscription: str) -> Union[StocksApiClient, CryptoApiClient]:
        return ApiClientFactory.from_market(market, subscription)
    
    
    def default_menu(self, options: list[str]) -> str:
        logger.debug(f"+default_menu()")
        
        cli_menu = TerminalMenu(options)
        selected_option_index = cli_menu.show()
        
        if isinstance(selected_option_index, int):
            selected_option = options[selected_option_index]
        
        else:
            msg = f"default_menu(): Unexpected output from .show(). Recevied {selected_option_index=}"
            logger.error(msg)
            raise ValueError(msg)
        
        logger.debug(f"-default_menu(): selected '{selected_option}'")
        return selected_option
    

    def get_symbol(self) -> str:
        logger.debug(f"+get_symbol()")
        
        symbol = input("Please enter the symbol to find the last recorded price: ")
        symbol = symbol.lower()
        
        logger.debug(f"-get_symbol()")
        return symbol
    

    def showcase_symbol_price(self, symbol: str, price: float) -> None:
        print(f"The last recorded price of '{symbol.upper()}' is $ {price}.")
    
