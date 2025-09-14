from typing import Union

from src.api_clients.stocks_api_client import StocksApiClient
from src.api_clients.crypto_api_client import CryptoApiClient

from src.constants import STR_STOCKS, STR_CRYPTO, STR_DEFAULT, STR_FREE, STR_PREMIUM

from src.logger import get_logger

logger = get_logger(__name__)


class ApiClientFactory:
    api_client_mapping = {
        STR_STOCKS: StocksApiClient.from_subscription_type,
        STR_CRYPTO: CryptoApiClient.from_subscription_type
    }


    @staticmethod
    def from_market(market: str, subscription: str) -> Union[StocksApiClient, CryptoApiClient]:
        api_client_class = ApiClientFactory.api_client_mapping.get(market)

        if api_client_class is not None:
            api_client = api_client_class(subscription)
        
        else:
            msg = "from_market(): Unable to fetch appropriate API client. Invalid market and subcription values"
            logger.error(msg)
            raise ValueError(msg)
        
        return api_client
