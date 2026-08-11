"""
Markets Terminal — Bloomberg-style
Run with: streamlit run app.py
"""

import streamlit as st
import config
import data_fetchers as fetch

IST = ZoneInfo("Asia/Kolkata")

st.set_page_config(page_title="Markets Terminal", layout="wide", initial_sidebar_state="expanded")

# ---------------- Bloomberg-terminal styling ----------------
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    * { font-family: 'Consolas', 'SF Mono', 'Courier New', monospace; }
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #ff9900; }

    .card { border: 1px solid #333; background: #000; margin-bottom: 6px; }
    .panel-bar {
        background: #ff9900; color: #000; font-weight: 700; font-size: 10.5px;
        text-transform: uppercase; letter-spacing: 0.06em; padding: 3px 8px;
        display: flex; justify-content: space-between;
    }
    .panel-body { padding: 4px 8px; }

    .row-line {
        display: flex; justify-content: space-between; align-items: center;
        padding: 2px 0; border-bottom: 1px solid #1a1a1a; font-size: 11.5px;
    }
    .row-line:last-child { border-bottom: none; }
    .rlabel { color: #ccc; }
    .rvalue { color: #fff; font-weight: 600; font-variant-numeric: tabular-nums; margin-left: auto; padding-right: 8px; }
    .rchg { font-variant-numeric: tabular-nums; width: 62px; text-align: right; font-weight: 600; }
    .up { color: #00ff41; } .down { color: #ff3333; } .flat { color: #888; }
    .caption-note { font-size: 9.5px; color: #666; margin-bottom: 3px; font-style: italic; }

    table { width: 100%; font-size: 11px; border-collapse: collapse; color: #e0e0e0; }
    td, th { padding: 3px 6px; border-right: 1px solid #1a1a1a; }
    td:last-child, th:last-child { border-right: none; }
    th { color: #ff9900; font-weight: 700; text-align: right; font-size: 9.5px; text-transform: uppercase;
         border-bottom: 1px solid #ff9900; background: #0a0a0a; }
    th:first-child, td:first-child { text-align: left; }
    tr { border-bottom: 1px solid #1a1a1a; }
    tr:hover td { background: #0d0d0d; }

    .sector-tile { padding: 5px; text-align: center; border: 1px solid #333; }
    .ticker-strip { display: flex; gap: 0; padding: 4px 8px; font-size: 12px; overflow-x: auto; align-items: center; }
    .ticker-item { padding-right: 14px; margin-right: 14px; border-right: 1px solid #333; }
    .status-badge {
        display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px; color: #00ff41;
        padding: 2px 8px; border: 1px solid #00ff41; margin-right: 14px; font-weight: 700;
    }
    .status-dot { width: 6px; height: 6px; border-radius: 50%; background: #00ff41; }
    .go-code { color: #ff9900; font-size: 10px; }
</style>
""", unsafe_allow_html=True)


# ---------------- cached data ----------------
@st.cache_data(ttl=config.REFRESH_SECONDS)
def load(kind):
    if kind == "top_ticker": return fetch.get_index_strip(config.TOP_TICKER)
    if kind == "global": return fetch.get_index_strip(config.GLOBAL_MARKETS)
    if kind == "india": return fetch.get_index_strip(config.INDIA_MARKETS)
    if kind == "pulse": return fetch.get_index_strip(config.MARKET_PULSE)
    if kind == "watchlist": return fetch.get_index_strip_with_sparkline(config.WATCHLIST)
    if kind == "gainers": return fetch.get_top_movers(config.MARKET_SCAN_CANDIDATES, gainers=True)
    if kind == "losers": return fetch.get_top_movers(config.MARKET_SCAN_CANDIDATES, gainers=False)
    if kind == "heatmap": return fetch.get_sector_heatmap(config.SECTOR_MAP)


# ---------------- helpers ----------------
def fmt_price(p):
    if p is None: return "N/A"
    return f"{p:,.2f}" if p < 1000 else f"{p:,.0f}"

def fmt_pct(p):
    if p is None: return "N/A"
    return f"{p:+.2f}%"

def cls(p):
    if p is None: return "flat"
    return "up" if p > 0 else ("down" if p < 0 else "flat")

def svg_spark(values, width=44, height=15):
    if not values or len(values) < 2:
        return ""
    lo, hi = min(values), max(values)
    rng = (hi - lo) or 1
    step = width / (len(values) - 1)
    pts = " ".join(f"{i*step:.1f},{height - ((v-lo)/rng)*height:.1f}" for i, v in enumerate(values))
    color = "#00ff41" if values[-1] >= values[0] else "#ff3333"
    return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="margin-left:6px">' \
           f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.3"/></svg>'

def render_rows(title, code, rows, spark=False):
    parts = [f'<div class="card"><div class="panel-bar"><span>{title}</span><span class="go-code">{code} &lt;GO&gt;</span></div><div class="panel-body">']
    for r in rows:
        s = svg_spark(r.get("spark", [])) if spark else ""
        parts.append(
            '<div class="row-line">'
            f'<span class="rlabel">{r["label"].upper()}</span>'
            f'<span class="rvalue">{fmt_price(r["price"])}</span>'
            f'<span class="rchg {cls(r["change_pct"])}">{fmt_pct(r["change_pct"])}</span>'
            f'{s}'
            '</div>'
        )
    parts.append('</div></div>')
    st.markdown(''.join(parts), unsafe_allow_html=True)

def panel_open(title, code=""):
    st.markdown(f'<div class="card"><div class="panel-bar"><span>{title}</span><span class="go-code">{code}</span></div><div class="panel-body">', unsafe_allow_html=True)

def panel_close():
    st.markdown('</div></div>', unsafe_allow_html=True)

def render_table(rows, columns):
    header = "".join(f"<th>{h}</th>" for h, _, _ in columns)
    body = ""
    for row in rows:
        cells = ""
        for h, key, fmtr in columns:
            val = row.get(key)
            shown = fmtr(val) if fmtr else val
            css = cls(val) if h == "CHG" else ""
            cells += f"<td class='{css}'>{shown}</td>"
        body += f"<tr>{cells}</tr>"
    st.markdown(f"<table><tr>{header}</tr>{body}</table>", unsafe_allow_html=True)


# ================= SIDEBAR =================
with st.sidebar:
    st.markdown('<div style="color:#ff9900;font-weight:700;font-size:14px;letter-spacing:0.08em;padding:8px 0">MARKETS<br>TERMINAL</div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top:1px solid #333;margin:6px 0"></div>', unsafe_allow_html=True)
    nav = [("F1", "OVERVIEW"), ("F2", "INDICES"), ("F3", "F&O"), ("F4", "FLOWS"),
           ("F5", "SECTORS"), ("F6", "NEWS"), ("F7", "ALERTS")]
    for key, label in nav:
        st.markdown(f'<div style=\'padding:4px 0;font-size:11px;color:#ccc\'><span style=\'color:#ff9900;font-weight:700\'>{key}</span> {label}</div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top:1px solid #333;margin:8px 0"></div>', unsafe_allow_html=True)
    if st.button("↻ REFRESH"):
        st.cache_data.clear()
        st.rerun()

# ================= TOP TICKER STRIP =================
ticker_row = load("top_ticker")
strip_html = f'<div class="ticker-strip"><span class="status-badge"><span class="status-dot"></span>MARKET OPEN</span>' \
             f'<span class="ticker-item" style="color:#666">{datetime.now().strftime("%H:%M:%S")} IST</span>'
for t in ticker_row:
    strip_html += f'<span class="ticker-item"><b style="color:#ff9900">{t["label"].upper()}</b> <span style="color:#fff">{fmt_price(t["price"])}</span> <span class="{cls(t["change_pct"])}">{fmt_pct(t["change_pct"])}</span></span>'
strip_html += "</div>"
st.markdown(f'<div class="card">{strip_html}</div>', unsafe_allow_html=True)

# ================= GLOBAL / INDIA / PULSE =================
c1, c2, c3 = st.columns(3)
with c1: render_rows("GLOBAL MARKETS", "WEI", load("global"))
with c2: render_rows("INDIA MARKETS", "IEI", load("india"))
with c3: render_rows("MARKET PULSE", "MOV", load("pulse"))

# ================= FLOWS & VALUATION (placeholder) =================
panel_open("FLOWS &amp; VALUATION", "FLOW")
st.markdown('<div class="caption-note">Placeholder — needs NSE derivatives statistics to go live</div>', unsafe_allow_html=True)
fcols = st.columns(len(config.FLOWS_PLACEHOLDER))
for col, item in zip(fcols, config.FLOWS_PLACEHOLDER):
    col.markdown(f'<div style="text-align:center"><div style="color:#888;font-size:9.5px;text-transform:uppercase">{item["label"]}</div><div class="{item["dir"]}" style="font-size:12px;font-weight:700">{item["value"]}</div></div>', unsafe_allow_html=True)
panel_close()

# ================= WATCHLIST / SECTOR HEATMAP =================
c4, c5 = st.columns([1.2, 1])
with c4:
    panel_open("WATCHLIST", "PRTF")
    render_table(load("watchlist"), [("STOCK", "label", None), ("PRICE", "price", fmt_price), ("CHG", "change_pct", fmt_pct)])
    panel_close()

    panel_open("SECTOR HEATMAP", "SCTR")
    heatmap = load("heatmap")
    hcols = st.columns(4)
    for i, sector in enumerate(heatmap):
        c = sector["change_pct"]
        bg = "#0a2e13" if c > 1 else "#061f0c" if c > 0 else "#3d0a0a" if c < -1 else "#2a0707" if c < 0 else "#111"
        with hcols[i % 4]:
            st.markdown(f'<div class="sector-tile" style="background:{bg}"><div style="font-size:9.5px;color:#ccc;text-transform:uppercase">{sector["label"]}</div><div class="{cls(c)}" style="font-size:11px;font-weight:700">{fmt_pct(c)}</div></div>', unsafe_allow_html=True)
    panel_close()

with c5:
    g1, g2 = st.columns(2)
    with g1:
        panel_open("GAINERS", "TOP+")
        render_table(load("gainers"), [("STOCK", "label", None), ("CHG", "change_pct", fmt_pct)])
        panel_close()
    with g2:
        panel_open("LOSERS", "TOP-")
        render_table(load("losers"), [("STOCK", "label", None), ("CHG", "change_pct", fmt_pct)])
        panel_close()

    panel_open("MACRO INDICATORS", "ECST")
    st.markdown('<div class="caption-note">Placeholder — needs a free FRED API key</div>', unsafe_allow_html=True)
    for m in config.MACRO_PLACEHOLDER:
        st.markdown(f'<div class="row-line"><span class="rlabel">{m["label"].upper()}</span><span class="rvalue" style="font-size:11px">{m["value"]}</span><span class="{m["dir"]}" style="width:48px;text-align:right;font-size:10px">{m["chg"]}</span></div>', unsafe_allow_html=True)
    panel_close()

# ================= FUTURES OI (placeholder) =================
panel_open("FUTURES OPEN INTEREST", "FOI")
st.markdown('<div class="caption-note">Placeholder — needs NSE F&amp;O bhavcopy data (via `nsepython`)</div>', unsafe_allow_html=True)
oi1, oi2 = st.columns([1, 2])
with oi1:
    st.markdown('<div style="color:#ff9900;font-size:10px;font-weight:700;margin-bottom:3px">INDEX FUTURES</div>', unsafe_allow_html=True)
    render_table(config.FUTURES_OI_PLACEHOLDER["index"],
                 [("INSTRUMENT", "instrument", None), ("LTP", "ltp", None), ("OI CHG", "oi_chg_pct", None), ("BIAS", "bias", None)])
with oi2:
    st.markdown('<div style="color:#ff9900;font-size:10px;font-weight:700;margin-bottom:3px">STOCK FUTURES</div>', unsafe_allow_html=True)
    render_table(config.FUTURES_OI_PLACEHOLDER["stock"],
                 [("INSTRUMENT", "instrument", None), ("PRICE", "price", None), ("OI CHG", "oi_chg_pct", None), ("BIAS", "bias", None)])
panel_close()

st.markdown('<div style="color:#444;font-size:9.5px">Prices via Yahoo Finance (yfinance), may be delayed. Placeholder sections clearly marked.</div>', unsafe_allow_html=True)
