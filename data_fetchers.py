"""
All live data pulls live here. Every function returns plain Python
dicts/lists so app.py doesn't need to know anything about yfinance.
"""

import yfinance as yf
import pandas as pd


def _pct_change(hist: pd.DataFrame) -> float:
    """Compute % change from previous close to latest close."""
    if len(hist) < 2:
        return 0.0
    prev_close = hist["Close"].iloc[-2]
    last_close = hist["Close"].iloc[-1]
    if prev_close == 0:
        return 0.0
    return (last_close - prev_close) / prev_close * 100


def get_quote(ticker: str) -> dict:
    """
    Fetch latest price + % change for a single ticker.
    Returns {"price": float, "change_pct": float} or None values on failure
    so the UI can show a clear "—" instead of crashing.
    """
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="5d", interval="1d")
        if hist.empty:
            return {"price": None, "change_pct": None}
        price = float(hist["Close"].iloc[-1])
        change_pct = _pct_change(hist)
        return {"price": price, "change_pct": change_pct}
    except Exception:
        return {"price": None, "change_pct": None}


def get_quote_with_volume(ticker: str) -> dict:
    """Same as get_quote but also returns latest day's volume."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="5d", interval="1d")
        if hist.empty:
            return {"price": None, "change_pct": None, "volume": None}
        price = float(hist["Close"].iloc[-1])
        change_pct = _pct_change(hist)
        volume = float(hist["Volume"].iloc[-1])
        return {"price": price, "change_pct": change_pct, "volume": volume}
    except Exception:
        return {"price": None, "change_pct": None, "volume": None}


def get_index_strip(label_ticker_map: dict) -> list:
    """
    For a dict like {"Nifty 50": "^NSEI", ...}, fetch each and return
    a list of dicts ready for direct rendering:
    [{"label": "Nifty 50", "price": 24981.2, "change_pct": 0.61}, ...]
    """
    results = []
    for label, ticker in label_ticker_map.items():
        q = get_quote(ticker)
        price = q["price"]
        # ^TNX (10y treasury) comes back as yield*10 from yfinance — fix it
        if ticker == "^TNX" and price is not None:
            price = price / 10
        results.append({"label": label, "price": price, "change_pct": q["change_pct"]})
    return results


def get_watchlist_table(label_ticker_map: dict) -> list:
    """Same shape as get_index_strip — reused for watchlist rendering."""
    return get_index_strip(label_ticker_map)


def get_most_active_table(candidates: dict, top_n: int = 5) -> list:
    """
    Fetch price/change/volume for every candidate, then return the
    top_n by volume — this is what makes it genuinely "most active"
    rather than just a fixed list.
    """
    rows = []
    for label, ticker in candidates.items():
        q = get_quote_with_volume(ticker)
        if q["volume"] is not None:
            rows.append({
                "label": label,
                "price": q["price"],
                "change_pct": q["change_pct"],
                "volume": q["volume"],
            })
    rows.sort(key=lambda r: r["volume"], reverse=True)
    return rows[:top_n]


def get_sparkline(ticker: str, period: str = "5d") -> list:
    """Return a list of closing prices for a small trend line. Empty list on failure."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period, interval="1d")
        if hist.empty:
            return []
        return [float(v) for v in hist["Close"].tolist()]
    except Exception:
        return []


def get_index_strip_with_sparkline(label_ticker_map: dict) -> list:
    """Same as get_index_strip, but each row also carries a 'spark' list."""
    results = get_index_strip(label_ticker_map)
    for row, (label, ticker) in zip(results, label_ticker_map.items()):
        row["spark"] = get_sparkline(ticker)
    return results


def get_top_movers(candidates: dict, top_n: int = 5, gainers: bool = True) -> list:
    """
    Rank the candidate pool by % change. Set gainers=False for top losers.
    NOTE: scans only the curated candidate list in config.py, not the
    full market — a true full-market scan needs NSE's daily bhavcopy.
    """
    rows = []
    for label, ticker in candidates.items():
        q = get_quote(ticker)
        if q["change_pct"] is not None:
            rows.append({"label": label, "price": q["price"], "change_pct": q["change_pct"]})
    rows.sort(key=lambda r: r["change_pct"], reverse=gainers)
    return rows[:top_n]


def get_top_gainers(candidates: dict, top_n: int = 5) -> list:
    """
    Rank the candidate pool by % change descending. NOTE: this only
    scans the curated candidate list in config.py, not the full market —
    a true full-market gainers scan needs NSE's daily bhavcopy file.
    """
    rows = []
    for label, ticker in candidates.items():
        q = get_quote(ticker)
        if q["change_pct"] is not None:
            rows.append({"label": label, "price": q["price"], "change_pct": q["change_pct"]})
    rows.sort(key=lambda r: r["change_pct"], reverse=True)
    return rows[:top_n]


def get_sector_heatmap(sector_map: dict) -> list:

    """
    Proxy sector performance as the average % change of a few
    representative stocks per sector. Not as precise as a true
    sector index, but works with zero extra data sources.
    """
    results = []
    for sector, tickers in sector_map.items():
        changes = []
        for ticker in tickers:
            q = get_quote(ticker)
            if q["change_pct"] is not None:
                changes.append(q["change_pct"])
        avg_change = sum(changes) / len(changes) if changes else 0.0
        results.append({"label": sector, "change_pct": avg_change})
    return results
