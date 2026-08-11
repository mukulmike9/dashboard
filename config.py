"""
Central config: every ticker and mapping the dashboard uses.
Edit this file to change your watchlist, tickers, sectors, etc.
"""

# ---- Top ticker strip — kept minimal on purpose: just the 3 numbers
# an Indian trader glances at first. Everything else (Bank Nifty, gold,
# silver, USD/INR) already lives in the panels below — repeating them
# here was just clutter. ----
TOP_TICKER = {
    "Nifty 50": "^NSEI",
    "Sensex": "^BSESN",
    "India VIX": "^INDIAVIX",
}

# ---- Global Markets panel — the indices that actually move Indian
# markets overnight (US close + European/Asian open cues) ----
GLOBAL_MARKETS = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "FTSE 100": "^FTSE",
    "Nikkei 225": "^N225",
}

# ---- India Markets panel ----
INDIA_MARKETS = {
    "Nifty 50": "^NSEI",
    "Sensex": "^BSESN",
    "Bank Nifty": "^NSEBANK",
    "Nifty Midcap 100": "NIFTYMIDCAP150.NS",  # coverage on yfinance is unreliable — verify on first run
    "GIFT Nifty": "NIFTY_FIN_SERVICE.NS",     # placeholder ticker — GIFT Nifty trades on NSE IX,
                                                # not reliably available via yfinance; will likely need
                                                # a different source (see README) — flagged clearly in UI too
}

# ---- Market Pulse panel ----
MARKET_PULSE = {
    "VIX": "^VIX",
    "10y UST": "^TNX",          # yfinance returns yield*10 — corrected in fetcher
    "DXY": "DX-Y.NYB",
    "USD/INR": "INR=X",
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Brent Crude": "BZ=F",
    "Copper": "HG=F",
    "Bitcoin": "BTC-USD",
}

# ---- Your personal watchlist ----
WATCHLIST = {
    "HDFC Bank": "HDFCBANK.NS",
    "Reliance": "RELIANCE.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Infosys": "INFY.NS",
    "TCS": "TCS.NS",
    "Larsen & Toubro": "LT.NS",
}

# ---- Candidate pool used for both "Most active" (by volume) and
# "Top gainers" (by % change). This is NOT a full market scan — it's
# a curated list of liquid, widely-tracked names. A true full-market
# gainers/losers scan needs NSE's daily bhavcopy (see README). ----
MARKET_SCAN_CANDIDATES = {
    "Tata Motors": "TATAMOTORS.NS", "SBI": "SBIN.NS", "Yes Bank": "YESBANK.NS",
    "Vodafone Idea": "IDEA.NS", "IDFC First": "IDFCFIRSTB.NS",
    "Tata Steel": "TATASTEEL.NS", "ITC": "ITC.NS", "Axis Bank": "AXISBANK.NS",
    "Adani Ports": "ADANIPORTS.NS", "Bajaj Finance": "BAJFINANCE.NS",
    "Adani Enterprises": "ADANIENT.NS", "M&M": "M&M.NS",
    "Wipro": "WIPRO.NS", "HCL Tech": "HCLTECH.NS", "Coal India": "COALINDIA.NS",
    "Tech Mahindra": "TECHM.NS", "Sun Pharma": "SUNPHARMA.NS",
}

# ---- Sector heatmap: sector -> representative stocks (performance
# proxied as the average % change of these stocks) ----
SECTOR_MAP = {
    "IT": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS"],
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
    "Auto": ["TATAMOTORS.NS", "MARUTI.NS", "M&M.NS", "BAJAJ-AUTO.NS"],
    "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS"],
    "FMCG": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
    "Metal": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS"],
    "Realty": ["DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS"],
    "PSU Bank": ["SBIN.NS", "BANKBARODA.NS", "PNB.NS", "CANBK.NS"],
    "Media": ["ZEEL.NS", "SUNTV.NS", "PVRINOX.NS"],
    "Cap Goods": ["LT.NS", "SIEMENS.NS", "ABB.NS"],
    "Cons Durable": ["TITAN.NS", "HAVELLS.NS", "VOLTAS.NS"],
}

REFRESH_SECONDS = 60

# ---- Placeholder blocks: real free live sources for these need either
# a FRED API key (macro) or NSE's raw daily files (flows/F&O). Structure
# matches what the UI expects so swapping in real data later is a
# one-function change, not a redesign. ----
MACRO_PLACEHOLDER = [
    {"label": "CPI (YoY)", "value": "2.90%", "chg": "-0.10", "dir": "down"},
    {"label": "Unemployment", "value": "4.10%", "chg": "Flat", "dir": "flat"},
    {"label": "RBI Repo Rate", "value": "6.50%", "chg": "Flat", "dir": "flat"},
    {"label": "IIP (YoY)", "value": "3.20%", "chg": "+0.20", "dir": "up"},
    {"label": "Fed Funds Rate", "value": "5.50%", "chg": "Flat", "dir": "flat"},
    {"label": "India 10Y Yield", "value": "6.92%", "chg": "Flat", "dir": "flat"},
]

FLOWS_PLACEHOLDER = [
    {"label": "FII (Cash)", "value": "-1,842 cr", "dir": "down"},
    {"label": "DII (Cash)", "value": "+2,105 cr", "dir": "up"},
    {"label": "FII Index Fut.", "value": "-1,265 cr", "dir": "down"},
    {"label": "FII Stock Fut.", "value": "-745 cr", "dir": "down"},
    {"label": "FII Index Opt.", "value": "+1,128 cr", "dir": "up"},
    {"label": "FII Stock Opt.", "value": "+1,342 cr", "dir": "up"},
]

FNO_SNAPSHOT_PLACEHOLDER = [
    {"label": "Index Futures", "pct": 38.2},
    {"label": "Index Options", "pct": 27.8},
    {"label": "Stock Futures", "pct": 18.1},
    {"label": "Stock Options", "pct": 15.9},
]

FUTURES_OI_PLACEHOLDER = {
    "index": [
        {"instrument": "Nifty Fut", "ltp": "24,995.00", "oi_chg_pct": "+2.35%", "bias": "Long Build"},
        {"instrument": "Bank Nifty Fut", "ltp": "56,412.00", "oi_chg_pct": "-1.02%", "bias": "Long Unwind"},
    ],
    "stock": [
        {"instrument": "Reliance Fut", "price": "2,991.20", "oi_chg_pct": "+2.48%", "bias": "Long Build"},
        {"instrument": "HDFC Bank Fut", "price": "1,715.10", "oi_chg_pct": "+1.35%", "bias": "Short Cover"},
        {"instrument": "Tata Steel Fut", "price": "168.40", "oi_chg_pct": "-2.05%", "bias": "Short Build"},
        {"instrument": "Infosys Fut", "price": "1,598.30", "oi_chg_pct": "+0.85%", "bias": "Long Build"},
        {"instrument": "SBI Fut", "price": "835.20", "oi_chg_pct": "-1.25%", "bias": "Long Unwind"},
    ],
}
