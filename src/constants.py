import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG').upper()

COIN_GECKO_SUBSCRIPTION = os.environ.get('COIN_GECKO_SUBSCRIPTION', 'FREE').upper()
COIN_GECKO_API_KEY      = os.environ.get('COIN_GECKO_API_KEY', '')

STR_GET     = "GET"
STR_POST    = "POST"

STR_FREE    = "FREE"
STR_PREMIUM = "PREMIUM"

# Crypto API related constants
COIN_GECKO_DEMO_API_URL         = "https://api.coingecko.com/api/v3/"
COIN_GECKO_DEMO_API_KEY_HEADER  = "x-cg-demo-api-key"
COIN_GECKO_PRO_API_URL          = "https://pro-api.coingecko.com/api/v3/"
COIN_GECKO_PRO_API_KEY_HEADER   = "x-cg-pro-api-key"

COIN_GECKO_SIMPLE_PRICE_ENDPOINT = "simple/price"
COIN_GECKO_SIMPLE_SUPPORTED_CRYPTO_ENDPOINT = "simple/supported_vs_currencies"

STR_USD = "usd"
STR_INR = "inr"
