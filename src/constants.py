import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG').upper()

STR_GET     = "GET"
STR_POST    = "POST"

LIST_SUPPORTED_HTTPS_METHODS = [STR_GET, STR_POST]

STR_FREE    = "FREE"
STR_PREMIUM = "PREMIUM"
