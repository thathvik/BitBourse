from typing import Union

from src.io_interface import IOInterface
from src.api_clients.stocks_api_client import StocksApiClient
from src.api_clients.crypto_api_client import CryptoApiClient

from src.logger import get_logger, setup_logging

# Set's up logging structure for the program before any logger calls 
# (by this point, all the loggers will have been defined in respective modules but not called)
setup_logging()

logger = get_logger(__name__)

def main():
    try:
        io_interface = IOInterface()

        api_client: Union[StocksApiClient, CryptoApiClient] = io_interface.pick_api_client()

        symbol = io_interface.get_symbol()

        price = api_client.get_price(symbol)

        io_interface.showcase_symbol_price(symbol, price)

    except Exception as global_exception:
        logger.error(f"main(): Unable to show the requested information. Global Exception Occured: {global_exception}")

    
if __name__ == "__main__":
    main()
