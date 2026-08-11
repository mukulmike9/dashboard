# Markets Terminal

Personal markets dashboard built with Streamlit. Tracks global/India indices,
watchlist, sector heatmap, gainers/losers — free data via yfinance.

## Setup

```
pip install -r requirements.txt
streamlit run app.py
```

## Deployment on (Streamlit Cloud, free)

URL. https://dashboard-euxvyfyw9fabtday7pnug3.streamlit.app/

## Files

- `app.py` — UI and layout
- `config.py` — watchlist, tickers, sectors — edit this to customize
- `data_fetchers.py` — data pulling logic
- `requirements.txt`

## Live vs placeholder

Live: top ticker, Global/India/Pulse panels, watchlist, gainers/losers, sector
heatmap.

Placeholder (static numbers, clearly marked in the UI): Flows & Valuation,
Macro Indicators, Futures OI. These need NSE derivatives data and a FRED API
key respectively — not available through a simple free API.

## Known issues

- GIFT Nifty and Nifty Midcap 100 may show N/A — unreliable yfinance coverage
- Gainers/Losers only scan the candidate list in `config.py`, not the full market

## Customize

Edit `config.py`: `WATCHLIST`, `SECTOR_MAP`, `GLOBAL_MARKETS`, `INDIA_MARKETS`,
`MARKET_PULSE`, `REFRESH_SECONDS`. Tickers use Yahoo Finance format — Indian
stocks need `.NS` suffix, indices start with `^`.
