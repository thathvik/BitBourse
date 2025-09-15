# BitBourse

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

A lightweight Python CLI to fetch live stock and cryptocurrency prices through an interactive terminal interface — no GUI. BitBourse provides a unified way to check market prices using Alpha Vantage for stocks and CoinGecko for cryptocurrencies.

## Features
- Stocks via Alpha Vantage (last daily close)
- Crypto via CoinGecko (USD quotes)
- Interactive terminal menu (simple-term-menu)
- Config via `.env` and environment variables
- Structured logging with configurable level

## Requirements

- Python 3.12+
- API Keys:
  - Alpha Vantage API key (required for stock prices)
  - CoinGecko API key (required for cryptocurrency prices)

## Installation
Clone and set up a virtual environment with an explicit Python 3.12+ interpreter.

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/BitBourse.git
cd BitBourse
```

### 2. Create a virtual environment and activate it:

macOS/Linux (prefer python3.13; fall back to 3.12 if needed)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell)
```powershell
py -m venv .venv 
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```
Interpreter note:
- Use a versioned interpreter (`python3.13` or `python3.12`) rather than a generic `python` alias to avoid picking an older system Python.
- Verify with `python --version` after activating your venv; it should show 3.12.x or 3.13.x.

### 4. Set up your API keys:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
LOG_LEVEL=DEBUG
COIN_GECKO_SUBSCRIPTION=FREE  # or PREMIUM
COIN_GECKO_API_KEY=your_coingecko_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

Notes:
- `LOG_LEVEL` supports `DEBUG`, `INFO`, `WARNING`, `ERROR`.

## Getting API Keys
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- CoinGecko (FREE/PRO): https://www.coingecko.com/en/developers/dashboard

## Usage
- Run the app:
  - `python app.py`  (ensure your venv uses Python 3.12+)

- Follow the prompts:
  - Pick market: Stocks or Crypto
  - If Crypto, choose FREE or PREMIUM subscription
  - Enter a symbol
    - Crypto examples: `btc`, `eth`, `ltc`
    - Stock examples: `aapl`, `msft`, `goog`

Example output:
- `The last recorded price of 'AAPL' is $ 156.42.`

## How It Works
- Stocks (Alpha Vantage)
  - Calls `TIME_SERIES_DAILY` and returns the most recent `4. close` price.
- Crypto (CoinGecko)
  - Calls `/simple/price` with `vs_currencies=usd` for your symbol list.
- Interactive input/display
  - Menus via `simple-term-menu`; symbols are normalized to lowercase.
- Logging
  - Centralized setup in `src/logger.py`; level controlled by `LOG_LEVEL`.

## Project Structure
```
BitBourse/
├── app.py                  # Main application entry point
├── src/
│   ├── api_clients/        # API client implementations
│   │   ├── base_api_client.py
│   │   ├── stocks_api_client.py
│   │   ├── crypto_api_client.py
│   │   └── api_client_factory.py
│   ├── io_interface.py     # Terminal menu and user interaction
│   ├── constants.py        # Configuration and constants
│   ├── utils.py           # Utility functions
│   └── logger.py          # Logging configuration
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── LICENSE                # MIT License
```

## Notes and Limitations
- Crypto symbol validation is currently disabled (`CryptoApiClient.SKIP_SYMBOL_VALIDATION = True`) due to an unreliable provider endpoint.
- Stocks return last daily close, not intraday.
- Behavior depends on third‑party APIs (latency, availability, rate limits).
- The terminal menu requires an interactive TTY.

## Troubleshooting
- HTTP errors or unexpected responses: verify API keys, provider status, and set `LOG_LEVEL=DEBUG`.
- Rate limits: Alpha Vantage free tier is strict; CoinGecko limits vary by plan.
- Terminal menu not showing: run in a real terminal; on Windows, prefer PowerShell/Windows Terminal.

## License
MIT — see [LICENSE](LICENSE).
