import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG').upper()

ALPHA_VATAGE_API_KEY = os.environ.get('ALPHA_VATAGE_API_KEY','')

STR_GET     = "GET"
STR_POST    = "POST"

LIST_SUPPORTED_HTTPS_METHODS = [STR_GET, STR_POST]

STR_FREE    = "FREE"
STR_PREMIUM = "PREMIUM"

# Stock API related constants
ALPHA_VANTAGE_API_URL           = "https://www.alphavantage.co/"
ALPHA_VANTAGE_API_KEY_PARAM     = "apikey"
ALPHA_VATAGE_API_QUERY_ENDPOINT = "query"

STR_TIME_SERIES_DAILY   = "TIME_SERIES_DAILY"

TIME_SERIES_DAILY_KEY   = "Time Series (Daily)"
CLOSE_KEY               = "4. close"
