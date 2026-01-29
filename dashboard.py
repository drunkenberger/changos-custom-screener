"""
OpenBB Stock & Options Dashboard
Dashboard personalizado para análisis de acciones y opciones
RAYGUN AESTHETIC EDITION
"""

import os
# Configure OpenBB to use /tmp for Streamlit Cloud compatibility
os.environ['OPENBB_HOME'] = '/tmp/openbb'

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Chango's Ultimate Screener",
    page_icon="🦍",
    layout="wide"
)

# === THEME SYSTEM ===
import raygun_theme as raygun

# Initialize theme in session state
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = 'Raygun'

# Apply theme from session state
raygun.set_theme(st.session_state.app_theme)

# Inject theme-specific CSS
st.markdown(raygun.get_dynamic_streamlit_css(st.session_state.app_theme), unsafe_allow_html=True)

# Inject appropriate CSS based on current theme (Corporate or Raygun)
raygun.inject_theme_css()

# === GLOSSARY DATA ===
from glossary_data import GLOSSARY_TERMS, get_glossary_html

# === HEDGE ANALYZER ===
import hedge_analyzer as hedge

# === FUND SCREENER ===
import fund_screener as funds

# === PORTFOLIO GENERATOR ===
import portfolio_generator as portfolio

# === GLOBAL FOOTER (theme-aware) ===
if st.session_state.app_theme != 'Corporate':
    st.markdown(raygun.get_global_footer("Creado por Drunkenberger"), unsafe_allow_html=True)

# Importar OpenBB
@st.cache_resource
def load_openbb():
    from openbb import obb
    return obb

obb = load_openbb()

# === MARKET TICKER BANNER ===
TICKER_SYMBOLS = [
    # Major Indices
    {"symbol": "^GSPC", "name": "S&P 500", "is_index": True},
    {"symbol": "^DJI", "name": "DOW 30", "is_index": True},
    {"symbol": "^IXIC", "name": "NASDAQ", "is_index": True},
    {"symbol": "^RUT", "name": "RUSSELL 2K", "is_index": True},
    {"symbol": "^VIX", "name": "VIX", "is_index": True},
    # Commodities
    {"symbol": "GC=F", "name": "GOLD", "is_commodity": True},
    {"symbol": "SI=F", "name": "SILVER", "is_commodity": True},
    {"symbol": "CL=F", "name": "CRUDE OIL", "is_commodity": True},
    {"symbol": "NG=F", "name": "NAT GAS", "is_commodity": True},
    {"symbol": "BTC-USD", "name": "BITCOIN", "is_commodity": True},
    # Top Stocks
    {"symbol": "AAPL", "name": "Apple"},
    {"symbol": "MSFT", "name": "Microsoft"},
    {"symbol": "GOOGL", "name": "Google"},
    {"symbol": "AMZN", "name": "Amazon"},
    {"symbol": "NVDA", "name": "NVIDIA"},
    {"symbol": "META", "name": "Meta"},
    {"symbol": "TSLA", "name": "Tesla"},
    {"symbol": "AMD", "name": "AMD"},
]

@st.cache_data(ttl=60)  # Cache for 60 seconds
def fetch_ticker_data():
    """Fetch real-time data for ticker symbols."""
    import yfinance as yf
    stocks_data = []

    try:
        for item in TICKER_SYMBOLS:
            sym = item["symbol"]
            try:
                ticker_obj = yf.Ticker(sym)
                info = ticker_obj.fast_info
                price = info.get('lastPrice', 0) or info.get('regularMarketPrice', 0)
                prev_close = info.get('previousClose', price)
                change = price - prev_close if prev_close else 0
                change_pct = (change / prev_close * 100) if prev_close else 0
                stocks_data.append({
                    'symbol': item.get('name', sym),
                    'price': price or 0,
                    'change': change,
                    'change_pct': change_pct,
                    'is_index': item.get('is_index', False),
                    'is_commodity': item.get('is_commodity', False)
                })
            except Exception:
                pass
    except Exception:
        # Fallback with sample data if API fails
        for item in TICKER_SYMBOLS:
            stocks_data.append({
                'symbol': item.get('name', item['symbol']),
                'price': 0,
                'change': 0,
                'change_pct': 0,
                'is_index': item.get('is_index', False),
                'is_commodity': item.get('is_commodity', False)
            })
    return stocks_data

# Header - full width title
# Dynamic title based on theme
if st.session_state.app_theme == 'Corporate':
    st.markdown(raygun.get_theme_title("Stock Analysis Platform", "Professional Market Intelligence"), unsafe_allow_html=True)
else:
    st.markdown(raygun.get_centered_title("CHANGO'S CUSTOM SCREENER", "POWERED BY OPENBB"), unsafe_allow_html=True)

# Display ticker banner below title (hidden in Corporate mode for cleaner look)
if st.session_state.app_theme != 'Corporate':
    ticker_data = fetch_ticker_data()
    if ticker_data:
        st.markdown(raygun.generate_ticker_html(ticker_data), unsafe_allow_html=True)

# === SIDEBAR - Tools & Info ===

# Market Status (at top of sidebar)
from datetime import datetime
import pytz
try:
    ny_tz = pytz.timezone('America/New_York')
    ny_time = datetime.now(ny_tz)
    market_hour = ny_time.hour
    market_minute = ny_time.minute
    is_weekday = ny_time.weekday() < 5
    is_market_hours = is_weekday and ((market_hour == 9 and market_minute >= 30) or (10 <= market_hour < 16))
    pre_market = is_weekday and (4 <= market_hour < 9 or (market_hour == 9 and market_minute < 30))
    after_hours = is_weekday and (16 <= market_hour < 20)

    if is_market_hours:
        status_color, status_text = "#39FF14", "🟢 MARKET OPEN"
    elif pre_market:
        status_color, status_text = "#FFE600", "🟡 PRE-MARKET"
    elif after_hours:
        status_color, status_text = "#FF6B35", "🟠 AFTER-HOURS"
    else:
        status_color, status_text = "#FF3366", "🔴 MARKET CLOSED"

    st.sidebar.markdown(f'<div style="font-family:Space Mono,monospace;font-size:1.1rem;color:{status_color};text-shadow:0 0 10px {status_color};padding:10px;text-align:center;border:2px solid {status_color};margin:5px 0 15px 0;background:rgba(13,13,13,0.9);">{status_text}<br><span style="font-size:0.85rem;color:#CCC;">{ny_time.strftime("%b %d, %Y")} | {ny_time.strftime("%H:%M:%S")} NY</span></div>', unsafe_allow_html=True)
except Exception:
    st.sidebar.markdown('<div style="color:#888;text-align:center;padding:10px;">Market status unavailable</div>', unsafe_allow_html=True)

st.sidebar.markdown(raygun.get_sidebar_title("RESEARCH", "TOOLS"), unsafe_allow_html=True)
st.sidebar.markdown(raygun.get_sidebar_section("Search"), unsafe_allow_html=True)

# Initialize session state for ticker
if 'ticker' not in st.session_state:
    st.session_state.ticker = "AAPL"

# Check for pending ticker update from quick access buttons
if 'pending_ticker' in st.session_state:
    st.session_state.ticker = st.session_state.pending_ticker
    del st.session_state.pending_ticker

ticker = st.sidebar.text_input("TICKER", value=st.session_state.ticker, placeholder="Enter symbol...").upper()
if ticker:
    st.session_state.ticker = ticker

# Quick access - horizontal rectangle buttons in 2 columns
st.sidebar.markdown(raygun.get_sidebar_section("Quick Access"), unsafe_allow_html=True)

# Initialize quick access tickers in session state
if 'quick_symbols' not in st.session_state:
    st.session_state.quick_symbols = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "AMD"]

quick_symbols = st.session_state.quick_symbols

# CSS: clean rectangles, no shadows, no pseudo-elements, with hover highlight
st.markdown("""
<style>
[data-testid="stSidebar"] .stButton > button {
    clip-path: none !important;
    transform: none !important;
    border-radius: 0 !important;
    white-space: nowrap !important;
    min-height: 38px !important;
    height: 38px !important;
    box-shadow: none !important;
    overflow: visible !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button::before,
[data-testid="stSidebar"] .stButton > button::after {
    display: none !important;
    content: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,255,255,0.3) !important;
    border-color: #00FFFF !important;
    box-shadow: 0 0 15px rgba(0,255,255,0.5), inset 0 0 10px rgba(0,255,255,0.2) !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button p {
    white-space: nowrap !important;
    overflow: visible !important;
}
</style>
""", unsafe_allow_html=True)

# 2 columns, 4 rows
for row in range(4):
    cols = st.sidebar.columns(2)
    idx1 = row * 2
    idx2 = row * 2 + 1
    if idx1 < len(quick_symbols):
        if cols[0].button(quick_symbols[idx1], key=f"quick_{quick_symbols[idx1]}", use_container_width=True):
            st.session_state.pending_ticker = quick_symbols[idx1]
            st.rerun()
    if idx2 < len(quick_symbols):
        if cols[1].button(quick_symbols[idx2], key=f"quick_{quick_symbols[idx2]}", use_container_width=True):
            st.session_state.pending_ticker = quick_symbols[idx2]
            st.rerun()

# Settings popover for editing quick access tickers
with st.sidebar.popover("⚙️ Edit Tickers", use_container_width=True):
    current_tickers = ", ".join(st.session_state.quick_symbols) if 'quick_symbols' in st.session_state else "AAPL, NVDA, TSLA, MSFT, GOOGL, AMZN, META, AMD"
    new_tickers = st.text_input("Tickers (comma separated)", value=current_tickers, key="quick_tickers_input")
    if st.button("Update Tickers", key="update_quick_tickers"):
        parsed = [t.strip().upper() for t in new_tickers.split(",") if t.strip()]
        if parsed:
            st.session_state.quick_symbols = parsed[:8]
            st.rerun()

# === CALCULATORS ===
st.sidebar.markdown(raygun.get_sidebar_section("Calculators"), unsafe_allow_html=True)
calc_type = st.sidebar.selectbox("Type", ["SL/TP Calculator", "Position Size", "Compound Interest", "Currency Exchange"], key="calc_type", label_visibility="collapsed")

if calc_type == "SL/TP Calculator":
    sltp_ticker = st.sidebar.text_input("Ticker", value=ticker, key="sltp_ticker").upper()
    sltp_cols1 = st.sidebar.columns(2)
    sltp_entry = sltp_cols1[0].number_input("Entry ($)", value=150.0, min_value=0.01, step=1.0, key="sltp_entry")
    sltp_direction = sltp_cols1[1].selectbox("Direction", ["LONG", "SHORT"], key="sltp_direction")
    sltp_rr = st.sidebar.selectbox("Risk/Reward", ["1:1", "1:2", "1:3", "1:4"], key="sltp_rr", index=1)

    # Fetch ATR for the ticker
    atr_value = None
    atr_pct = 2.0  # Default fallback
    try:
        hist_data = obb.equity.price.historical(sltp_ticker, provider="yfinance", period="1mo", interval="1d")
        df_hist = hist_data.to_dataframe()
        if not df_hist.empty and len(df_hist) >= 14:
            # Calculate ATR (14-period)
            df_hist['hl'] = df_hist['high'] - df_hist['low']
            df_hist['hc'] = abs(df_hist['high'] - df_hist['close'].shift(1))
            df_hist['lc'] = abs(df_hist['low'] - df_hist['close'].shift(1))
            df_hist['tr'] = df_hist[['hl', 'hc', 'lc']].max(axis=1)
            atr_value = df_hist['tr'].rolling(14).mean().iloc[-1]
            current_price = df_hist['close'].iloc[-1]
            atr_pct = (atr_value / current_price) * 100
    except Exception:
        pass

    # Calculate SL/TP based on ATR or percentage
    rr_multiplier = {"1:1": 1, "1:2": 2, "1:3": 3, "1:4": 4}[sltp_rr]

    if atr_value:
        sl_distance = atr_value * 1.5  # 1.5x ATR for SL
        tp_distance = sl_distance * rr_multiplier
        atr_display = f"ATR(14): ${atr_value:.2f} ({atr_pct:.1f}%)"
    else:
        sl_distance = sltp_entry * 0.02  # 2% fallback
        tp_distance = sl_distance * rr_multiplier
        atr_display = "ATR: N/A (using 2%)"

    if sltp_direction == "LONG":
        sl_price = sltp_entry - sl_distance
        tp_price = sltp_entry + tp_distance
    else:
        sl_price = sltp_entry + sl_distance
        tp_price = sltp_entry - tp_distance

    sl_pct = abs(sltp_entry - sl_price) / sltp_entry * 100
    tp_pct = abs(tp_price - sltp_entry) / sltp_entry * 100

    st.sidebar.markdown(f'<div style="font-size:0.75rem;color:#888;margin:4px 0;">{atr_display}</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div style="background:rgba(255,51,102,0.15);border:1px solid #FF3366;padding:8px;margin-top:4px;"><div style="color:#888;font-size:0.7rem;">STOP LOSS</div><div style="color:#FF3366;font-size:1.2rem;font-family:Bebas Neue,sans-serif;">${sl_price:.2f}</div><div style="color:#FF3366;font-size:0.75rem;">-{sl_pct:.1f}% from entry</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div style="background:rgba(57,255,20,0.15);border:1px solid #39FF14;padding:8px;margin-top:4px;"><div style="color:#888;font-size:0.7rem;">TAKE PROFIT</div><div style="color:#39FF14;font-size:1.2rem;font-family:Bebas Neue,sans-serif;">${tp_price:.2f}</div><div style="color:#39FF14;font-size:0.75rem;">+{tp_pct:.1f}% from entry</div></div>', unsafe_allow_html=True)

elif calc_type == "Compound Interest":
    ci_principal = st.sidebar.number_input("Principal ($)", value=10000.0, min_value=0.0, step=100.0, key="ci_principal")
    ci_cols = st.sidebar.columns(2)
    ci_rate = ci_cols[0].number_input("Rate (%)", value=7.0, min_value=0.0, max_value=100.0, step=0.5, key="ci_rate")
    ci_years = ci_cols[1].number_input("Years", value=10, min_value=1, max_value=50, step=1, key="ci_years")
    ci_compound = st.sidebar.selectbox("Frequency", ["Monthly", "Quarterly", "Annually"], key="ci_compound")
    n_periods = {"Monthly": 12, "Quarterly": 4, "Annually": 1}[ci_compound]
    ci_result = ci_principal * (1 + (ci_rate/100)/n_periods) ** (n_periods * ci_years)
    ci_gain = ci_result - ci_principal
    st.sidebar.markdown(f'<div style="background:rgba(57,255,20,0.1);border:1px solid #39FF14;padding:8px;margin-top:6px;"><div style="color:#39FF14;font-size:1.3rem;font-family:Bebas Neue,sans-serif;">${ci_result:,.2f}</div><div style="color:#00FFFF;font-size:0.8rem;">+${ci_gain:,.2f} ({(ci_gain/ci_principal)*100:.1f}%)</div></div>', unsafe_allow_html=True)

elif calc_type == "Currency Exchange":
    cx_amount = st.sidebar.number_input("Amount", value=1000.0, min_value=0.0, step=10.0, key="cx_amount")
    cx_cols = st.sidebar.columns(2)
    cx_from = cx_cols[0].selectbox("From", ["USD", "EUR", "GBP", "JPY", "MXN", "CAD", "CHF"], key="cx_from")
    cx_to = cx_cols[1].selectbox("To", ["MXN", "EUR", "GBP", "JPY", "USD", "CAD", "CHF"], key="cx_to")
    rates_to_usd = {"USD": 1, "EUR": 1.08, "GBP": 1.27, "JPY": 0.0067, "MXN": 0.058, "CAD": 0.74, "CHF": 1.13}
    usd_to_rates = {"USD": 1, "EUR": 0.93, "GBP": 0.79, "JPY": 149.5, "MXN": 17.2, "CAD": 1.35, "CHF": 0.88}
    if cx_from == cx_to:
        cx_result = cx_amount
    else:
        usd_value = cx_amount * rates_to_usd[cx_from]
        cx_result = usd_value * usd_to_rates[cx_to]
    rate_display = cx_result / cx_amount if cx_amount > 0 else 0
    st.sidebar.markdown(f'<div style="background:rgba(0,255,255,0.1);border:1px solid #00FFFF;padding:8px;margin-top:6px;"><div style="color:#00FFFF;font-size:1.3rem;font-family:Bebas Neue,sans-serif;">{cx_result:,.2f} {cx_to}</div><div style="color:#FF00FF;font-size:0.8rem;">1 {cx_from} = {rate_display:.4f} {cx_to}</div></div>', unsafe_allow_html=True)

elif calc_type == "Position Size":
    ps_cols1 = st.sidebar.columns(2)
    ps_capital = ps_cols1[0].number_input("Capital ($)", value=25000.0, min_value=0.0, step=1000.0, key="ps_capital")
    ps_risk_pct = ps_cols1[1].number_input("Risk (%)", value=2.0, min_value=0.1, max_value=10.0, step=0.5, key="ps_risk")
    ps_cols2 = st.sidebar.columns(2)
    ps_entry = ps_cols2[0].number_input("Entry ($)", value=150.0, min_value=0.01, step=1.0, key="ps_entry")
    ps_stop = ps_cols2[1].number_input("Stop ($)", value=145.0, min_value=0.01, step=1.0, key="ps_stop")
    ps_risk_amount = ps_capital * (ps_risk_pct / 100)
    ps_risk_per_share = abs(ps_entry - ps_stop)
    ps_shares = int(ps_risk_amount / ps_risk_per_share) if ps_risk_per_share > 0 else 0
    ps_position_value = ps_shares * ps_entry
    st.sidebar.markdown(f'<div style="background:rgba(255,0,255,0.1);border:1px solid #FF00FF;padding:8px;margin-top:6px;"><div style="color:#FF00FF;font-size:1.3rem;font-family:Bebas Neue,sans-serif;">{ps_shares} shares</div><div style="color:#E0E0E0;font-size:0.8rem;">${ps_position_value:,.2f} | Risk: ${ps_risk_amount:,.2f}</div></div>', unsafe_allow_html=True)

# Settings
st.sidebar.markdown(raygun.get_sidebar_section("Settings"), unsafe_allow_html=True)

# Theme selector with Corporate option
theme_options = ["Raygun", "Dark", "Light", "Corporate"]
current_theme_index = theme_options.index(st.session_state.app_theme) if st.session_state.app_theme in theme_options else 0

selected_theme = st.sidebar.selectbox(
    "Theme",
    options=theme_options,
    index=current_theme_index,
    key="theme_selector",
    help="Raygun: Chaotic neon | Dark: Clean dark | Light: Professional light | Corporate: Elegant for clients"
)

# Update theme if changed
if selected_theme != st.session_state.app_theme:
    st.session_state.app_theme = selected_theme
    raygun.set_theme(selected_theme)
    st.rerun()

show_volume = st.sidebar.checkbox("Show Volume", value=True)
show_emas = st.sidebar.checkbox("Show EMAs", value=True)

# Función para formatear números grandes como currency
def format_market_cap(value):
    """Formatea números grandes con notación de currency (K, M, B, T)."""
    if value is None:
        return "N/A"

    # Si ya es un número, usarlo directamente
    if isinstance(value, (int, float)):
        num_value = float(value)
    else:
        # Intentar convertir de string
        try:
            # Remover caracteres de formato ($, comas, espacios)
            str_value = str(value).replace('$', '').replace(',', '').replace(' ', '').strip()

            # Manejar sufijos existentes (B, M, K, T)
            multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3}
            for suffix, mult in multipliers.items():
                if str_value.upper().endswith(suffix):
                    num_value = float(str_value[:-1]) * mult
                    break
            else:
                num_value = float(str_value)
        except (ValueError, TypeError):
            return str(value) if value else "N/A"

    # Formatear con notación apropiada
    if num_value >= 1_000_000_000_000:  # Trillones
        return f"${num_value / 1_000_000_000_000:,.2f}T"
    elif num_value >= 1_000_000_000:  # Billones
        return f"${num_value / 1_000_000_000:,.2f}B"
    elif num_value >= 1_000_000:  # Millones
        return f"${num_value / 1_000_000:,.2f}M"
    elif num_value >= 1_000:  # Miles
        return f"${num_value / 1_000:,.2f}K"
    else:
        return f"${num_value:,.2f}"

# Función para calcular POC y niveles de liquidación
def calculate_poc_and_levels(df, current_price):
    """Calculate Point of Control (POC) and key liquidity levels."""
    if df is None or len(df) < 20:
        return None
    try:
        price_range = df['high'].max() - df['low'].min()
        num_bins = 50
        bin_size = price_range / num_bins
        bins = {}
        for _, row in df.iterrows():
            low = row['low']
            high = row['high']
            vol = row['volume']
            price_levels = int((high - low) / bin_size) + 1
            vol_per_level = vol / max(price_levels, 1)
            for i in range(price_levels):
                price_level = round((low + i * bin_size) / bin_size) * bin_size
                bins[price_level] = bins.get(price_level, 0) + vol_per_level
        if not bins:
            return None
        poc = max(bins, key=bins.get)
        total_volume = sum(bins.values())
        sorted_bins = sorted(bins.items(), key=lambda x: x[1], reverse=True)
        cumulative_vol = 0
        value_area_prices = []
        for price, vol in sorted_bins:
            cumulative_vol += vol
            value_area_prices.append(price)
            if cumulative_vol >= total_volume * 0.7:
                break
        value_area_high = max(value_area_prices) if value_area_prices else poc
        value_area_low = min(value_area_prices) if value_area_prices else poc
        liquidation_levels = []
        base = 10 ** (len(str(int(current_price))) - 2)
        for i in range(-5, 6):
            level = round(current_price / base) * base + i * base
            if level > 0:
                liquidation_levels.append({'price': level, 'type': 'ROUND', 'delta': ((level - current_price) / current_price) * 100})
        liquidation_levels.append({'price': poc, 'type': 'POC', 'delta': ((poc - current_price) / current_price) * 100})
        liquidation_levels.append({'price': value_area_high, 'type': 'VAH', 'delta': ((value_area_high - current_price) / current_price) * 100})
        liquidation_levels.append({'price': value_area_low, 'type': 'VAL', 'delta': ((value_area_low - current_price) / current_price) * 100})
        liquidation_levels.sort(key=lambda x: abs(x['delta']))
        return {'poc': poc, 'value_area_high': value_area_high, 'value_area_low': value_area_low, 'levels': liquidation_levels[:8], 'volume_profile': bins}
    except:
        return None

# === TAB PERSISTENCE ===
# JavaScript robusto con MutationObserver para persistir tabs
tab_persistence_js = """
<script>
(function() {
    const TAB_STORAGE_KEY = 'dashboard_active_tab';

    function getStoredTab() {
        // Primero verificar URL
        const urlParams = new URLSearchParams(window.location.search);
        const urlTab = urlParams.get('tab');
        if (urlTab !== null) return parseInt(urlTab);

        // Luego localStorage
        const stored = localStorage.getItem(TAB_STORAGE_KEY);
        if (stored !== null) return parseInt(stored);

        return 0;
    }

    function saveTab(index) {
        localStorage.setItem(TAB_STORAGE_KEY, index);
        const url = new URL(window.location);
        url.searchParams.set('tab', index);
        window.history.replaceState({}, '', url);
    }

    function setupTabs() {
        const tabs = document.querySelectorAll('[data-baseweb="tab"]');
        if (tabs.length < 8) return false;

        const savedTab = getStoredTab();

        // Click en el tab guardado si no es el primero
        if (savedTab > 0 && savedTab < tabs.length) {
            const targetTab = tabs[savedTab];
            const isSelected = targetTab.getAttribute('aria-selected') === 'true';
            if (!isSelected) {
                targetTab.click();
            }
        }

        // Configurar listeners
        tabs.forEach(function(tab, index) {
            if (!tab.dataset.persistListener) {
                tab.dataset.persistListener = 'true';
                tab.addEventListener('click', function() {
                    saveTab(index);
                });
            }
        });

        return true;
    }

    // MutationObserver para detectar cuando los tabs están listos
    const observer = new MutationObserver(function(mutations) {
        if (setupTabs()) {
            observer.disconnect();
        }
    });

    // Observar el body para cambios
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // También intentar inmediatamente y con delays
    setupTabs();
    setTimeout(setupTabs, 100);
    setTimeout(setupTabs, 300);
    setTimeout(setupTabs, 500);

    // Desconectar observer después de 5 segundos para no afectar performance
    setTimeout(function() { observer.disconnect(); }, 5000);
})();
</script>
"""
st.markdown(tab_persistence_js, unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🏢 Perfil", "📈 Precios", "📊 Opciones", "📋 Financieros", "🎯 Análisis", "🛡️ Hedge", "📦 Fondos", "💼 Portfolio"])

# TAB 1: Perfil de la Empresa
with tab1:
    # Fetch current price for header
    try:
        from datetime import datetime, timedelta
        price_end = datetime.now().strftime('%Y-%m-%d')
        price_start = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        price_info = obb.equity.price.historical(symbol=ticker, start_date=price_start, end_date=price_end, provider="yfinance")
        price_df = price_info.to_dataframe()
        if not price_df.empty:
            current_px = price_df['close'].iloc[-1]
            prev_px = price_df['close'].iloc[-2] if len(price_df) > 1 else current_px
            delta_pct = ((current_px - prev_px) / prev_px) * 100
            delta_color = '#00FF88' if delta_pct >= 0 else '#FF3366'
            delta_sign = '+' if delta_pct >= 0 else ''
            st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;"><h2 style="margin:0;color:#E0E0E0;">Perfil de {ticker}</h2><div style="background:linear-gradient(135deg,rgba(255,0,255,0.15) 0%,rgba(0,255,255,0.1) 100%);border:2px solid {delta_color};padding:12px 20px;display:flex;align-items:center;gap:15px;box-shadow:0 0 20px {delta_color}40;"><span style="font-size:2rem;color:#FF00FF;font-weight:bold;text-shadow:0 0 15px #FF00FF;">${current_px:.2f}</span><span style="font-size:1.3rem;color:{delta_color};font-weight:bold;text-shadow:0 0 10px {delta_color};padding:5px 10px;background:{delta_color}20;border-left:3px solid {delta_color};">{delta_sign}{delta_pct:.2f}%</span></div></div>', unsafe_allow_html=True)
        else:
            st.header(f"Perfil de {ticker}")
    except:
        st.header(f"Perfil de {ticker}")

    try:
        with st.spinner("Cargando perfil..."):
            profile = obb.equity.profile(ticker)
            df_profile = profile.to_dataframe()

            if not df_profile.empty:
                # Métricas principales en cards (4 columnas)
                st.subheader("Métricas Clave")
                cols = st.columns(4)

                with cols[0]:
                    val = df_profile.get('market_cap', pd.Series([None])).iloc[0]
                    st.metric("Market Cap", format_market_cap(val))

                with cols[1]:
                    val = df_profile.get('beta', pd.Series([None])).iloc[0]
                    display = f"{val:.2f}" if isinstance(val, (int, float)) else str(val) if val else "N/A"
                    st.metric("Beta", display)

                with cols[2]:
                    val = df_profile.get('employees', pd.Series([None])).iloc[0]
                    display = f"{int(val):,}" if isinstance(val, (int, float)) else str(val) if val else "N/A"
                    st.metric("Empleados", display)

                with cols[3]:
                    val = df_profile.get('earnings_date', pd.Series([None])).iloc[0]
                    st.metric("Earnings Date", val if val else "N/A")

                # === INSTITUTIONAL OWNERSHIP BANNER ===
                val = df_profile.get('institutional_ownership', pd.Series([None])).iloc[0]
                current_pct = float(val)*100 if isinstance(val, (int, float)) else None

                # Get institutional data
                inst_change = None
                num_institutions = 0
                total_inst_shares = 0
                insider_pct = None
                short_pct_float = None
                buying_count = 0
                selling_count = 0

                try:
                    import yfinance as yf
                    yf_ticker = yf.Ticker(ticker)

                    # Get institutional holders
                    inst_holders = yf_ticker.institutional_holders
                    if inst_holders is not None and not inst_holders.empty:
                        num_institutions = len(inst_holders)
                        if 'Shares' in inst_holders.columns:
                            total_inst_shares = inst_holders['Shares'].sum()

                        # Check for change columns
                        change_col = None
                        for col in inst_holders.columns:
                            if 'change' in col.lower() or 'chg' in col.lower():
                                change_col = col
                                break

                        if change_col:
                            for val in inst_holders[change_col]:
                                try:
                                    if pd.notna(val):
                                        v = float(str(val).replace('%', '').replace(',', ''))
                                        if v > 0:
                                            buying_count += 1
                                        elif v < 0:
                                            selling_count += 1
                                except:
                                    pass

                    # Get info for more data
                    info = yf_ticker.info
                    if info:
                        held_pct_inst = info.get('heldPercentInstitutions')
                        held_pct_insider = info.get('heldPercentInsiders')
                        if held_pct_inst:
                            current_pct = held_pct_inst * 100
                        if held_pct_insider:
                            insider_pct = held_pct_insider * 100

                        short_pct_float = info.get('shortPercentOfFloat')
                        if short_pct_float:
                            short_pct_float = short_pct_float * 100

                except Exception as e:
                    pass

                # Determine signal based on multiple factors
                signal_desc = ""

                # Calculate net sentiment from buying vs selling institutions
                if buying_count > 0 or selling_count > 0:
                    total_activity = buying_count + selling_count
                    if total_activity > 0:
                        buy_ratio = buying_count / total_activity
                        if buy_ratio > 0.7:
                            inst_signal = "HEAVY BUYING"
                            signal_desc = f"{buying_count} institutions adding positions"
                            signal_color = "#39FF14"
                        elif buy_ratio > 0.55:
                            inst_signal = "BUYING"
                            signal_desc = f"{buying_count} buying vs {selling_count} selling"
                            signal_color = "#00FF88"
                        elif buy_ratio < 0.3:
                            inst_signal = "HEAVY SELLING"
                            signal_desc = f"{selling_count} institutions reducing positions"
                            signal_color = "#FF3366"
                        elif buy_ratio < 0.45:
                            inst_signal = "SELLING"
                            signal_desc = f"{selling_count} selling vs {buying_count} buying"
                            signal_color = "#FF6B35"
                        else:
                            inst_signal = "MIXED"
                            signal_desc = f"Split: {buying_count} buying, {selling_count} selling"
                            signal_color = "#FFE600"
                else:
                    # Fallback: use ownership level + short interest
                    if current_pct is not None:
                        if current_pct > 85:
                            inst_signal = "HEAVILY OWNED"
                            signal_desc = "Very high institutional interest"
                            signal_color = "#39FF14"
                        elif current_pct > 70:
                            inst_signal = "WELL OWNED"
                            signal_desc = "Strong institutional support"
                            signal_color = "#00FF88"
                        elif current_pct > 50:
                            inst_signal = "MODERATE"
                            signal_desc = "Average institutional presence"
                            signal_color = "#00FFFF"
                        elif current_pct > 25:
                            inst_signal = "LIGHT"
                            signal_desc = "Below average inst. ownership"
                            signal_color = "#FFE600"
                        else:
                            inst_signal = "RETAIL HEAVY"
                            signal_desc = "Mostly retail ownership"
                            signal_color = "#FF6B35"
                    else:
                        inst_signal = "NO DATA"
                        signal_desc = "Unable to fetch ownership data"
                        signal_color = "#888888"

                # Build extra info HTML
                extra_info = ""
                if num_institutions > 0:
                    extra_info += f'<div style="text-align:center;padding:0 20px;border-left:1px solid rgba(255,255,255,0.1);"><div style="font-size:0.65rem;color:#888;"># INSTITUTIONS</div><div style="font-size:1.2rem;color:#E0E0E0;">{num_institutions}</div></div>'
                if insider_pct is not None:
                    extra_info += f'<div style="text-align:center;padding:0 20px;border-left:1px solid rgba(255,255,255,0.1);"><div style="font-size:0.65rem;color:#888;">INSIDER</div><div style="font-size:1.2rem;color:#FF00FF;">{insider_pct:.1f}%</div></div>'
                if short_pct_float is not None:
                    short_color = "#FF3366" if short_pct_float > 10 else "#FFE600" if short_pct_float > 5 else "#00FF88"
                    extra_info += f'<div style="text-align:center;padding:0 20px;border-left:1px solid rgba(255,255,255,0.1);"><div style="font-size:0.65rem;color:#888;">SHORT %</div><div style="font-size:1.2rem;color:{short_color};">{short_pct_float:.1f}%</div></div>'

                # Render the banner
                pct_display = f"{current_pct:.1f}" if current_pct else "N/A"

                banner_html = f'<div style="background:linear-gradient(90deg,rgba(26,26,46,0.95) 0%,rgba(13,13,13,0.98) 50%,rgba(26,26,46,0.95) 100%);border:1px solid {signal_color};border-left:5px solid {signal_color};padding:15px 25px;margin:15px 0;display:flex;align-items:center;justify-content:space-between;box-shadow:0 0 20px {signal_color}30;"><div style="display:flex;align-items:center;gap:20px;"><div><div style="font-size:0.65rem;color:#888;text-transform:uppercase;letter-spacing:0.1em;">INSTITUTIONAL OWNERSHIP</div><div style="font-size:2rem;color:#FF00FF;font-family:Bebas Neue,sans-serif;">{pct_display}%</div></div><div style="background:{signal_color}20;border:1px solid {signal_color};padding:8px 15px;text-align:center;"><div style="font-size:0.65rem;color:#888;">SIGNAL</div><div style="font-size:1.1rem;color:{signal_color};font-weight:bold;text-shadow:0 0 10px {signal_color};">{inst_signal}</div><div style="font-size:0.6rem;color:#aaa;margin-top:2px;">{signal_desc}</div></div></div><div style="display:flex;align-items:center;">{extra_info}</div></div>'

                st.markdown(banner_html, unsafe_allow_html=True)

                st.markdown("---")

                # Información en columnas
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Información General")

                    name = df_profile.get('name', pd.Series([None])).iloc[0]
                    if name:
                        st.write(f"**Nombre:** {name}")

                    sector = df_profile.get('sector', pd.Series([None])).iloc[0]
                    if sector:
                        st.write(f"**Sector:** {sector}")

                    industry = df_profile.get('industry_category', pd.Series([None])).iloc[0]
                    if industry:
                        st.write(f"**Industria:** {industry}")

                    country = df_profile.get('hq_country', pd.Series([None])).iloc[0]
                    if country:
                        st.write(f"**País:** {country}")

                    exchange = df_profile.get('stock_exchange', pd.Series([None])).iloc[0]
                    if exchange:
                        st.write(f"**Exchange:** {exchange}")

                    index_val = df_profile.get('index', pd.Series([None])).iloc[0]
                    if index_val:
                        st.write(f"**Índices:** {index_val}")

                    # POC & Niveles Clave section
                    st.markdown("---")
                    st.subheader("📊 POC & Niveles Clave (3M)")
                    try:
                        from datetime import datetime, timedelta
                        start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
                        end_date = datetime.now().strftime('%Y-%m-%d')
                        price_data = obb.equity.price.historical(symbol=ticker, start_date=start_date, end_date=end_date, provider="yfinance")
                        price_df = price_data.to_dataframe()
                        if not price_df.empty:
                            current_price = price_df['close'].iloc[-1]
                            poc_data = calculate_poc_and_levels(price_df, current_price)
                            if poc_data:
                                poc = poc_data['poc']
                                vah = poc_data['value_area_high']
                                val = poc_data['value_area_low']
                                poc_delta = ((poc - current_price) / current_price) * 100
                                vah_delta = ((vah - current_price) / current_price) * 100
                                val_delta = ((val - current_price) / current_price) * 100
                                poc_delta_color = '#00FF88' if poc_delta > 0 else '#FF3366'
                                vah_delta_color = '#00FF88' if vah_delta > 0 else '#FF3366'
                                val_delta_color = '#00FF88' if val_delta > 0 else '#FF3366'
                                st.markdown(f'<div style="background:rgba(255,0,255,0.1);border-left:3px solid #FF00FF;padding:10px;margin:4px 0;"><div style="color:#FF00FF;font-weight:bold;font-size:0.75rem;">POC (Point of Control)</div><div style="color:#E0E0E0;font-size:1.1rem;">${poc:.2f} <span style="color:{poc_delta_color};font-size:0.85rem;">({poc_delta:+.2f}%)</span></div></div>', unsafe_allow_html=True)
                                st.markdown(f'<div style="background:rgba(0,255,255,0.1);border-left:3px solid #00FFFF;padding:10px;margin:4px 0;"><div style="color:#00FFFF;font-weight:bold;font-size:0.75rem;">VAH (Value Area High)</div><div style="color:#E0E0E0;font-size:1.1rem;">${vah:.2f} <span style="color:{vah_delta_color};font-size:0.85rem;">({vah_delta:+.2f}%)</span></div></div>', unsafe_allow_html=True)
                                st.markdown(f'<div style="background:rgba(0,255,136,0.1);border-left:3px solid #00FF88;padding:10px;margin:4px 0;"><div style="color:#00FF88;font-weight:bold;font-size:0.75rem;">VAL (Value Area Low)</div><div style="color:#E0E0E0;font-size:1.1rem;">${val:.2f} <span style="color:{val_delta_color};font-size:0.85rem;">({val_delta:+.2f}%)</span></div></div>', unsafe_allow_html=True)
                                st.markdown("<div style='font-size:0.7rem;color:#888;margin-top:8px;'>🎯 Niveles de Liquidación</div>", unsafe_allow_html=True)
                                for lvl in poc_data['levels'][:5]:
                                    if lvl['type'] == 'ROUND':
                                        lvl_delta_color = '#00FF88' if lvl['delta'] > 0 else '#FF3366'
                                        st.markdown(f"<div style='background:rgba(136,136,136,0.1);padding:5px 10px;margin:2px 0;font-size:0.85rem;'><span style='color:#888;'>${lvl['price']:.2f}</span> <span style='color:{lvl_delta_color};'>({lvl['delta']:+.2f}%)</span></div>", unsafe_allow_html=True)
                            else:
                                st.info("No se pudo calcular POC")
                        else:
                            st.info("Sin datos de precios")
                    except Exception as e:
                        st.warning(f"Error calculando POC: {str(e)}")

                with col2:
                    st.subheader("Métricas de Acciones")

                    shares_out = df_profile.get('shares_outstanding', pd.Series([None])).iloc[0]
                    if shares_out:
                        st.write(f"**Acciones en Circulación:** {shares_out}")

                    shares_float = df_profile.get('shares_float', pd.Series([None])).iloc[0]
                    if shares_float:
                        st.write(f"**Shares Float:** {shares_float}")

                    short_interest = df_profile.get('short_interest', pd.Series([None])).iloc[0]
                    if short_interest:
                        st.write(f"**Short Interest:** {short_interest}")

                    inst_own = df_profile.get('institutional_ownership', pd.Series([None])).iloc[0]
                    if inst_own:
                        pct = float(inst_own) * 100 if isinstance(inst_own, (int, float)) else inst_own
                        st.write(f"**Propiedad Institucional:** {pct:.1f}%")

                    # Institutional Holdings Details (restored to original)
                    try:
                        import yfinance as yf
                        yf_ticker = yf.Ticker(ticker)
                        inst_holders = yf_ticker.institutional_holders
                        if inst_holders is not None and not inst_holders.empty:
                            st.markdown("---")
                            st.subheader("🏦 Top Instituciones")
                            top_5 = inst_holders.head(5)
                            for _, row in top_5.iterrows():
                                holder = row.get('Holder', 'N/A')
                                shares = row.get('Shares', 0)
                                value = row.get('Value', 0)
                                pct_out = row.get('% Out', 0)
                                st.markdown(f'<div style="background:rgba(0,255,255,0.05);border-left:3px solid #00FFFF;padding:8px 12px;margin:4px 0;font-size:0.85rem;"><div style="color:#00FFFF;font-weight:bold;">{holder}</div><div style="color:#888;">Shares: {shares:,.0f} | {pct_out*100:.2f}% | ${value:,.0f}</div></div>', unsafe_allow_html=True)
                    except:
                        pass

                # Descripción
                st.markdown("---")
                desc = df_profile.get('long_description', pd.Series([None])).iloc[0]
                if desc:
                    st.subheader("Descripción de la Empresa")
                    # Styled description with better line-height and readability
                    st.markdown(f'''
                    <div style="
                        line-height: 1.8;
                        color: #E0E0E0;
                        font-size: 0.95rem;
                        text-align: justify;
                        padding: 12px 0;
                        max-height: 300px;
                        overflow-y: auto;
                    ">{desc}</div>
                    ''', unsafe_allow_html=True)
            else:
                st.warning("No se encontró información del perfil")

    except Exception as e:
        st.error(f"Error al cargar perfil: {str(e)}")

# Función para limpiar duplicados de los resultados de OpenBB
def clean_openbb_results(results):
    seen_dates = set()
    clean = []
    for item in results:
        date_key = str(item.date) if hasattr(item, 'date') else str(item)
        if date_key not in seen_dates:
            seen_dates.add(date_key)
            clean.append(item)
    return clean

# Función para detectar divergencias bullish
def find_bullish_divergences(df, rsi_series, lookback=5, min_distance=3):
    """
    Detecta divergencias bullish: precio hace lower low, RSI hace higher low
    """
    divergences = []

    if rsi_series is None or len(rsi_series) < lookback * 2:
        return divergences

    # Alinear índices
    common_idx = df.index.intersection(rsi_series.index)
    if len(common_idx) < lookback * 2:
        return divergences

    price = df.loc[common_idx, 'low']
    rsi = rsi_series.loc[common_idx]

    # Encontrar mínimos locales en precio
    def find_local_mins(series, window=lookback):
        mins = []
        for i in range(window, len(series) - window):
            if series.iloc[i] == series.iloc[i-window:i+window+1].min():
                mins.append(i)
        return mins

    price_mins = find_local_mins(price)

    # Buscar divergencias bullish
    for i in range(1, len(price_mins)):
        idx1 = price_mins[i-1]
        idx2 = price_mins[i]

        # Verificar distancia mínima
        if idx2 - idx1 < min_distance:
            continue

        # Precio hace lower low
        price_lower_low = price.iloc[idx2] < price.iloc[idx1]

        # RSI hace higher low
        rsi_higher_low = rsi.iloc[idx2] > rsi.iloc[idx1]

        if price_lower_low and rsi_higher_low:
            divergences.append({
                'date': price.index[idx2],
                'price': price.iloc[idx2],
                'rsi': rsi.iloc[idx2],
                'prev_date': price.index[idx1],
                'prev_price': price.iloc[idx1],
                'prev_rsi': rsi.iloc[idx1]
            })

    return divergences

# Función para detectar divergencias bearish
def find_bearish_divergences(df, rsi_series, lookback=5, min_distance=3):
    """
    Detecta divergencias bearish: precio hace higher high, RSI hace lower high
    """
    divergences = []

    if rsi_series is None or len(rsi_series) < lookback * 2:
        return divergences

    # Alinear índices
    common_idx = df.index.intersection(rsi_series.index)
    if len(common_idx) < lookback * 2:
        return divergences

    price = df.loc[common_idx, 'high']
    rsi = rsi_series.loc[common_idx]

    # Encontrar máximos locales en precio
    def find_local_maxs(series, window=lookback):
        maxs = []
        for i in range(window, len(series) - window):
            if series.iloc[i] == series.iloc[i-window:i+window+1].max():
                maxs.append(i)
        return maxs

    price_maxs = find_local_maxs(price)

    # Buscar divergencias bearish
    for i in range(1, len(price_maxs)):
        idx1 = price_maxs[i-1]
        idx2 = price_maxs[i]

        # Verificar distancia mínima
        if idx2 - idx1 < min_distance:
            continue

        # Precio hace higher high
        price_higher_high = price.iloc[idx2] > price.iloc[idx1]

        # RSI hace lower high
        rsi_lower_high = rsi.iloc[idx2] < rsi.iloc[idx1]

        if price_higher_high and rsi_lower_high:
            divergences.append({
                'date': price.index[idx2],
                'price': price.iloc[idx2],
                'rsi': rsi.iloc[idx2],
                'prev_date': price.index[idx1],
                'prev_price': price.iloc[idx1],
                'prev_rsi': rsi.iloc[idx1]
            })

    return divergences


def calculate_momentum_state(df, ema_data=None):
    """
    Calculate momentum state based on multiple indicators.
    Returns: state, color, description
    """
    if df is None or len(df) < 50:
        return "INSUFFICIENT DATA", "#888888", "Not enough data to calculate momentum"

    close = df['close']

    # Calculate MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    # Calculate RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Get current values
    current_rsi = rsi.iloc[-1]
    current_macd = macd.iloc[-1]
    current_signal = signal.iloc[-1]
    current_histogram = histogram.iloc[-1]
    prev_histogram = histogram.iloc[-2] if len(histogram) > 1 else 0

    # Check histogram trend (last 3 bars)
    hist_trend = histogram.iloc[-3:].tolist() if len(histogram) >= 3 else [0, 0, 0]
    hist_increasing = hist_trend[-1] > hist_trend[-2] > hist_trend[-3]
    hist_decreasing = hist_trend[-1] < hist_trend[-2] < hist_trend[-3]

    # Check for recent MACD crossovers (last 5 bars)
    recent_bull_cross = False
    recent_bear_cross = False
    for i in range(-5, -1):
        if len(macd) > abs(i) and len(signal) > abs(i):
            if macd.iloc[i-1] < signal.iloc[i-1] and macd.iloc[i] > signal.iloc[i]:
                recent_bull_cross = True
            if macd.iloc[i-1] > signal.iloc[i-1] and macd.iloc[i] < signal.iloc[i]:
                recent_bear_cross = True

    # EMA alignment check
    ema_bullish = False
    ema_bearish = False
    if ema_data and len(ema_data) >= 2:
        emas = sorted(ema_data.items(), key=lambda x: x[0])
        current_price = close.iloc[-1]
        short_ema = list(ema_data.values())[0].iloc[-1] if len(list(ema_data.values())[0]) > 0 else current_price
        if current_price > short_ema:
            ema_bullish = True
        else:
            ema_bearish = True

    # Determine momentum state
    # FULLY BULLISH: RSI > 60, MACD > Signal, histogram positive & increasing, price > EMAs
    if current_rsi > 60 and current_macd > current_signal and current_histogram > 0 and hist_increasing and ema_bullish:
        return "FULLY BULLISH", "#39FF14", "Strong upward momentum across all indicators"

    # FULLY BEARISH: RSI < 40, MACD < Signal, histogram negative & decreasing, price < EMAs
    if current_rsi < 40 and current_macd < current_signal and current_histogram < 0 and hist_decreasing and ema_bearish:
        return "FULLY BEARISH", "#FF3366", "Strong downward momentum across all indicators"

    # RECENTLY TURNED BULLISH: Recent MACD bull cross, RSI > 50
    if recent_bull_cross and current_rsi > 50:
        return "RECENTLY TURNED BULLISH", "#00FF88", "MACD just crossed bullish, momentum shifting up"

    # RECENTLY TURNED BEARISH: Recent MACD bear cross, RSI < 50
    if recent_bear_cross and current_rsi < 50:
        return "RECENTLY TURNED BEARISH", "#FF6B35", "MACD just crossed bearish, momentum shifting down"

    # STARTING TO FLIP BULLISH: MACD approaching signal from below, histogram improving
    if current_macd < current_signal and current_histogram > prev_histogram and current_rsi > 45:
        return "STARTING TO FLIP BULLISH", "#FFE600", "Early signs of bullish reversal forming"

    # STARTING TO FLIP BEARISH: MACD approaching signal from above, histogram weakening
    if current_macd > current_signal and current_histogram < prev_histogram and current_rsi < 55:
        return "STARTING TO FLIP BEARISH", "#FF9500", "Early signs of bearish reversal forming"

    # BULLISH: RSI > 50, MACD > Signal
    if current_rsi > 50 and current_macd > current_signal:
        return "BULLISH", "#00FFFF", "Positive momentum, trend favors upside"

    # BEARISH: RSI < 50, MACD < Signal
    if current_rsi < 50 and current_macd < current_signal:
        return "BEARISH", "#FF00FF", "Negative momentum, trend favors downside"

    # NEUTRAL
    return "NEUTRAL", "#888888", "Mixed signals, no clear momentum direction"


# TAB 2: Precios Históricos
with tab2:
    st.header(f"Precios Históricos - {ticker}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        timeframe = st.selectbox("Timeframe:", ["15m", "30m", "1h", "2h", "Daily", "Weekly"], index=4)
    with col2:
        period = st.selectbox("Período:", ["5D", "1M", "3M", "6M", "1Y", "2Y"], index=3)
    with col3:
        chart_type = st.selectbox("Tipo de gráfico:", ["Candlestick", "Línea"])
    with col4:
        show_emas = st.multiselect("EMAs:", [20, 50, 100, 200], default=[20, 50, 200])

    col5, col6, col7 = st.columns(3)
    with col5:
        show_vwap = st.checkbox("VWAP", value=True)
    with col6:
        show_bull_div = st.checkbox("Bullish Divergences", value=True)
    with col7:
        show_bear_div = st.checkbox("Bearish Divergences", value=True)

    # Mapeo de timeframes a intervalos de OpenBB
    timeframe_map = {
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "2h": "90m",  # No hay 2h, usamos 90m como aproximación
        "Daily": "1d",
        "Weekly": "1d"  # Agregamos manualmente
    }

    period_map = {"5D": 5, "1M": 30, "3M": 90, "6M": 180, "1Y": 365, "2Y": 730}

    # Limitar período para timeframes intraday (yfinance tiene límites)
    if timeframe in ["15m", "30m"]:
        max_days = 60
        if period_map[period] > max_days:
            st.warning(f"Para {timeframe}, el período máximo es ~60 días. Ajustando...")
            period = "1M"
    elif timeframe in ["1h", "2h"]:
        max_days = 730
        if period_map[period] > max_days:
            period = "2Y"

    try:
        with st.spinner("Cargando precios..."):
            from datetime import datetime, timedelta
            # Pedir más datos para calcular EMAs correctamente
            extra_days = 250 if show_emas and timeframe in ["Daily", "Weekly"] else 50
            start = (datetime.now() - timedelta(days=period_map[period] + extra_days)).strftime("%Y-%m-%d")

            interval = timeframe_map[timeframe]
            data = obb.equity.price.historical(ticker, start_date=start, interval=interval, provider='yfinance')
            df = data.to_dataframe()

            if not df.empty:
                # Eliminar duplicados en el índice
                df = df[~df.index.duplicated(keep='first')]

                # Convertir a Weekly si es necesario
                if timeframe == "Weekly":
                    df_weekly = df.resample('W').agg({
                        'open': 'first',
                        'high': 'max',
                        'low': 'min',
                        'close': 'last',
                        'volume': 'sum'
                    }).dropna()
                    df = df_weekly

                # Calcular EMAs y RSI - RAYGUN COLORS
                ema_colors = raygun.EMA_COLORS
                ema_data = {}
                rsi_series = None

                if timeframe == "Weekly":
                    # Para weekly, calcular EMAs directamente del df resampleado
                    for ema_length in show_emas:
                        df[f'ema_{ema_length}'] = df['close'].ewm(span=ema_length, adjust=False).mean()
                        ema_data[ema_length] = df[f'ema_{ema_length}']
                    # RSI para weekly
                    delta = df['close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_series = 100 - (100 / (1 + rs))
                else:
                    # Calcular indicadores con pandas/ta (sin depender de obb.technical)
                    from ta.trend import EMAIndicator
                    from ta.momentum import RSIIndicator

                    for ema_length in show_emas:
                        try:
                            ema_indicator = EMAIndicator(close=df['close'], window=ema_length)
                            ema_data[ema_length] = ema_indicator.ema_indicator()
                        except Exception as e:
                            st.warning(f"No se pudo calcular EMA {ema_length}: {e}")

                    # RSI con ta library
                    try:
                        rsi_indicator = RSIIndicator(close=df['close'], window=14)
                        rsi_series = rsi_indicator.rsi()
                    except Exception as e:
                        st.warning(f"No se pudo calcular RSI: {e}")

                # Calcular VWAP (manual - no depende de obb.technical)
                vwap_series = None
                if show_vwap:
                    try:
                        typical_price = (df['high'] + df['low'] + df['close']) / 3
                        vwap_series = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
                    except Exception as e:
                        st.warning(f"No se pudo calcular VWAP: {e}")

                # Recortar datos al período seleccionado
                cutoff_date = (datetime.now() - timedelta(days=period_map[period])).date()
                df = df[pd.to_datetime(df.index).date >= cutoff_date]

                # Para Weekly, recalcular ema_data y rsi del df filtrado
                if timeframe == "Weekly":
                    ema_data = {}
                    for ema_length in show_emas:
                        if f'ema_{ema_length}' in df.columns:
                            ema_data[ema_length] = df[f'ema_{ema_length}']
                    # RSI ya está recortado porque es calculado sobre df
                    delta = df['close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi_series = 100 - (100 / (1 + rs))
                else:
                    for ema_length in list(ema_data.keys()):
                        ema_data[ema_length] = ema_data[ema_length][pd.to_datetime(ema_data[ema_length].index).date >= cutoff_date]
                    if rsi_series is not None:
                        rsi_series = rsi_series[pd.to_datetime(rsi_series.index).date >= cutoff_date]
                    if vwap_series is not None:
                        vwap_series = vwap_series[pd.to_datetime(vwap_series.index).date >= cutoff_date]

                # Para Weekly, recalcular VWAP del df filtrado
                if timeframe == "Weekly" and show_vwap:
                    typical_price = (df['high'] + df['low'] + df['close']) / 3
                    vwap_series = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()

                # === MOMENTUM INDICATOR ===
                momentum_state, momentum_color, momentum_desc = calculate_momentum_state(df, ema_data)

                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(26,26,46,0.95) 0%, rgba(13,13,13,0.98) 100%);
                    border: 2px solid {momentum_color};
                    border-left: 6px solid {momentum_color};
                    padding: 12px 20px;
                    margin: 10px 0 20px 0;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    box-shadow: 0 0 20px {momentum_color}40;
                ">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div style="
                            font-family: 'Bebas Neue', sans-serif;
                            font-size: 0.85rem;
                            color: #888;
                            text-transform: uppercase;
                            letter-spacing: 0.1em;
                        ">MOMENTUM</div>
                        <div style="
                            font-family: 'Bebas Neue', sans-serif;
                            font-size: 1.4rem;
                            color: {momentum_color};
                            text-shadow: 0 0 10px {momentum_color};
                            letter-spacing: 0.05em;
                        ">{momentum_state}</div>
                    </div>
                    <div style="
                        font-family: 'Space Mono', monospace;
                        font-size: 0.75rem;
                        color: #E0E0E0;
                        max-width: 400px;
                        text-align: right;
                    ">{momentum_desc}</div>
                </div>
                """, unsafe_allow_html=True)

                # === ÍNDICE SECUENCIAL PARA ELIMINAR GAPS ===
                # Crear mapeo de fechas a índice numérico secuencial
                df = df.reset_index()
                df['seq_idx'] = range(len(df))
                date_col = df.columns[0]  # Primera columna es la fecha original

                # Crear mapeo de fecha a índice secuencial
                date_to_seq = dict(zip(df[date_col], df['seq_idx']))

                # Preparar etiquetas para el eje X (mostrar cada N fechas)
                n_ticks = min(20, len(df))
                tick_step = max(1, len(df) // n_ticks)
                tickvals = list(range(0, len(df), tick_step))
                ticktext = [str(df[date_col].iloc[i])[:10] for i in tickvals]

                # Crear gráfico con 3 subplots: Precio, Volumen, RSI
                fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                                   vertical_spacing=0.05,
                                   row_heights=[0.6, 0.2, 0.2])

                # Gráfico de precios (usando índice secuencial) - RAYGUN STYLE
                candle_colors = raygun.get_candlestick_colors()
                if chart_type == "Candlestick":
                    fig.add_trace(go.Candlestick(
                        x=df['seq_idx'], open=df['open'], high=df['high'],
                        low=df['low'], close=df['close'], name=ticker,
                        increasing_line_color=candle_colors['increasing_line_color'],
                        decreasing_line_color=candle_colors['decreasing_line_color'],
                        increasing_fillcolor=candle_colors['increasing_fillcolor'],
                        decreasing_fillcolor=candle_colors['decreasing_fillcolor'],
                        customdata=df[date_col],
                        hovertemplate='%{customdata}<br>O: %{open}<br>H: %{high}<br>L: %{low}<br>C: %{close}<extra></extra>'
                    ), row=1, col=1)
                else:
                    fig.add_trace(go.Scatter(
                        x=df['seq_idx'], y=df['close'], mode='lines', name=ticker,
                        line=dict(color=raygun.COLORS['neon_cyan'], width=2),
                        customdata=df[date_col],
                        hovertemplate='%{customdata}<br>Precio: %{y:.2f}<extra></extra>'
                    ), row=1, col=1)

                # Agregar EMAs (mapeando índices)
                for ema_length, ema_s in ema_data.items():
                    # Mapear fechas de EMA al índice secuencial
                    ema_x = [date_to_seq.get(d, None) for d in ema_s.index]
                    ema_x_valid = [(x, y) for x, y in zip(ema_x, ema_s.values) if x is not None]
                    if ema_x_valid:
                        ema_x_vals, ema_y_vals = zip(*ema_x_valid)
                        fig.add_trace(go.Scatter(
                            x=list(ema_x_vals),
                            y=list(ema_y_vals),
                            mode='lines',
                            name=f'EMA {ema_length}',
                            line=dict(color=ema_colors[ema_length], width=1.5)
                        ), row=1, col=1)

                # Agregar VWAP (mapeando índices)
                if vwap_series is not None and len(vwap_series) > 0:
                    vwap_x = [date_to_seq.get(d, None) for d in vwap_series.index]
                    vwap_x_valid = [(x, y) for x, y in zip(vwap_x, vwap_series.values) if x is not None]
                    if vwap_x_valid:
                        vwap_x_vals, vwap_y_vals = zip(*vwap_x_valid)
                        fig.add_trace(go.Scatter(
                            x=list(vwap_x_vals),
                            y=list(vwap_y_vals),
                            mode='lines',
                            name='VWAP',
                            line=dict(color='#00FFFF', width=2, dash='dot')
                        ), row=1, col=1)

                # Volumen - RAYGUN COLORS
                vol_colors = raygun.get_volume_colors(df)
                fig.add_trace(go.Bar(x=df['seq_idx'], y=df['volume'], name='Volumen',
                                    marker_color=vol_colors, opacity=0.8), row=2, col=1)

                # RSI (mapeando índices) - RAYGUN STYLE
                if rsi_series is not None and len(rsi_series) > 0:
                    rsi_x = [date_to_seq.get(d, None) for d in rsi_series.index]
                    rsi_x_valid = [(x, y) for x, y in zip(rsi_x, rsi_series.values) if x is not None]
                    if rsi_x_valid:
                        rsi_x_vals, rsi_y_vals = zip(*rsi_x_valid)
                        fig.add_trace(go.Scatter(
                            x=list(rsi_x_vals),
                            y=list(rsi_y_vals),
                            mode='lines',
                            name='RSI',
                            line=dict(color=raygun.COLORS['purple_haze'], width=2)
                        ), row=3, col=1)

                    # Líneas de sobrecompra/sobreventa - RAYGUN COLORS
                    fig.add_hline(y=70, line_dash="dash", line_color=raygun.COLORS['hot_pink'],
                                 annotation_text="OVERBOUGHT (70)", row=3, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color=raygun.COLORS['neon_green'],
                                 annotation_text="OVERSOLD (30)", row=3, col=1)
                    fig.add_hline(y=50, line_dash="dot", line_color=raygun.COLORS['text_muted'], row=3, col=1)

                    # Detectar y marcar Bullish Divergences
                    # Necesitamos crear un df temporal con índice de fecha para las funciones de divergencia
                    df_for_div = df.set_index(date_col)

                    if show_bull_div:
                        bull_divs = find_bullish_divergences(df_for_div, rsi_series)

                        if bull_divs:
                            for div in bull_divs:
                                # Mapear fechas al índice secuencial
                                seq_date = date_to_seq.get(div['date'], None)
                                seq_prev = date_to_seq.get(div['prev_date'], None)

                                if seq_date is not None:
                                    # Marcador en el precio (triángulo verde hacia arriba) - RAYGUN
                                    fig.add_trace(go.Scatter(
                                        x=[seq_date],
                                        y=[div['price'] * 0.995],
                                        mode='markers+text',
                                        marker=dict(symbol='triangle-up', size=15, color=raygun.COLORS['neon_green']),
                                        text=['BULL'],
                                        textposition='bottom center',
                                        textfont=dict(color=raygun.COLORS['neon_green'], size=10, family='Space Mono'),
                                        name='Bullish Divergence',
                                        showlegend=False,
                                        hovertemplate=f"<b>BULLISH DIVERGENCE</b><br>Precio: ${div['price']:.2f}<br>RSI: {div['rsi']:.1f}<extra></extra>"
                                    ), row=1, col=1)

                                if seq_date is not None and seq_prev is not None:
                                    # Línea conectando los dos puntos en precio
                                    fig.add_trace(go.Scatter(
                                        x=[seq_prev, seq_date],
                                        y=[div['prev_price'], div['price']],
                                        mode='lines',
                                        line=dict(color=raygun.COLORS['neon_green'], width=2, dash='dash'),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ), row=1, col=1)

                                    # Línea conectando los dos puntos en RSI
                                    fig.add_trace(go.Scatter(
                                        x=[seq_prev, seq_date],
                                        y=[div['prev_rsi'], div['rsi']],
                                        mode='lines',
                                        line=dict(color=raygun.COLORS['neon_green'], width=2, dash='dash'),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ), row=3, col=1)

                            # Alerta de divergencias recientes
                            recent_bull = [d for d in bull_divs if (pd.Timestamp.now() - pd.Timestamp(d['date'])).days < 10]
                            if recent_bull:
                                st.success(f">>> {len(recent_bull)} BULLISH DIVERGENCE(S) DETECTED IN LAST 10 DAYS <<<")

                    # Detectar y marcar Bearish Divergences
                    if show_bear_div:
                        bear_divs = find_bearish_divergences(df_for_div, rsi_series)

                        if bear_divs:
                            for div in bear_divs:
                                # Mapear fechas al índice secuencial
                                seq_date = date_to_seq.get(div['date'], None)
                                seq_prev = date_to_seq.get(div['prev_date'], None)

                                if seq_date is not None:
                                    # Marcador en el precio (triángulo rojo hacia abajo) - RAYGUN
                                    fig.add_trace(go.Scatter(
                                        x=[seq_date],
                                        y=[div['price'] * 1.005],
                                        mode='markers+text',
                                        marker=dict(symbol='triangle-down', size=15, color=raygun.COLORS['hot_pink']),
                                        text=['BEAR'],
                                        textposition='top center',
                                        textfont=dict(color=raygun.COLORS['hot_pink'], size=10, family='Space Mono'),
                                        name='Bearish Divergence',
                                        showlegend=False,
                                        hovertemplate=f"<b>BEARISH DIVERGENCE</b><br>Precio: ${div['price']:.2f}<br>RSI: {div['rsi']:.1f}<extra></extra>"
                                    ), row=1, col=1)

                                if seq_date is not None and seq_prev is not None:
                                    # Línea conectando los dos puntos en precio
                                    fig.add_trace(go.Scatter(
                                        x=[seq_prev, seq_date],
                                        y=[div['prev_price'], div['price']],
                                        mode='lines',
                                        line=dict(color=raygun.COLORS['hot_pink'], width=2, dash='dash'),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ), row=1, col=1)

                                    # Línea conectando los dos puntos en RSI
                                    fig.add_trace(go.Scatter(
                                        x=[seq_prev, seq_date],
                                        y=[div['prev_rsi'], div['rsi']],
                                        mode='lines',
                                        line=dict(color=raygun.COLORS['hot_pink'], width=2, dash='dash'),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ), row=3, col=1)

                            # Alerta de divergencias recientes
                            recent_bear = [d for d in bear_divs if (pd.Timestamp.now() - pd.Timestamp(d['date'])).days < 10]
                            if recent_bear:
                                st.warning(f">>> {len(recent_bear)} BEARISH DIVERGENCE(S) DETECTED IN LAST 10 DAYS <<<")

                # === POC & VALUE AREA LINES (with hover) ===
                current_price = df['close'].iloc[-1]
                df_for_poc = df.set_index(date_col) if date_col in df.columns else df
                poc_result = calculate_poc_and_levels(df_for_poc, current_price)
                if poc_result:
                    poc = poc_result['poc']
                    vah = poc_result['value_area_high']
                    val = poc_result['value_area_low']
                    # Use all x values so hover works anywhere on the line
                    x_all = df['seq_idx'].tolist()
                    # POC line (magenta) - horizontal line with hover
                    fig.add_trace(go.Scatter(
                        x=x_all, y=[poc] * len(x_all), mode='lines',
                        name=f'POC ${poc:.2f}',
                        line=dict(color='#FF00FF', width=2, dash='dash'),
                        hovertemplate=f'POC: ${poc:.2f}<extra></extra>'
                    ), row=1, col=1)
                    # VAH line (cyan) - horizontal line with hover
                    fig.add_trace(go.Scatter(
                        x=x_all, y=[vah] * len(x_all), mode='lines',
                        name=f'VAH ${vah:.2f}',
                        line=dict(color='#00FFFF', width=1.5, dash='dot'),
                        hovertemplate=f'VAH: ${vah:.2f}<extra></extra>'
                    ), row=1, col=1)
                    # VAL line (green) - horizontal line with hover
                    fig.add_trace(go.Scatter(
                        x=x_all, y=[val] * len(x_all), mode='lines',
                        name=f'VAL ${val:.2f}',
                        line=dict(color='#00FF88', width=1.5, dash='dot'),
                        hovertemplate=f'VAL: ${val:.2f}<extra></extra>'
                    ), row=1, col=1)

                # Apply RAYGUN template
                fig.update_layout(
                    title=dict(text=''),  # Empty title to avoid "undefined"
                    xaxis_rangeslider_visible=False,
                    height=900,
                    margin=dict(t=80, l=60, r=150, b=60),
                    paper_bgcolor=raygun.COLORS['bg_dark'],
                    plot_bgcolor=raygun.COLORS['bg_dark'],
                    font=dict(family='Space Mono, monospace', color=raygun.COLORS['text_light']),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.04,
                        xanchor="left",
                        x=0.02,
                        bgcolor='rgba(13,13,13,0.95)',
                        bordercolor=raygun.COLORS['neon_pink'],
                        borderwidth=2,
                        font=dict(size=11, family='Space Mono, monospace', color='#FFFFFF'),
                        itemsizing='constant',
                        tracegroupgap=10
                    ),
                    dragmode='zoom',
                    hoverlabel=dict(
                        bgcolor=raygun.COLORS['bg_card'],
                        bordercolor=raygun.COLORS['neon_pink'],
                        font=dict(family='Space Mono', color=raygun.COLORS['text_light'])
                    ),
                    modebar=dict(
                        bgcolor='rgba(13,13,13,0.8)',
                        color=raygun.COLORS['neon_cyan'],
                        activecolor=raygun.COLORS['neon_pink'],
                        orientation='v'
                    )
                )

                # Clear any existing annotations and add custom subplot titles
                fig.layout.annotations = []
                fig.add_annotation(
                    text="<b>VOLUMEN</b>",
                    xref="paper", yref="paper",
                    x=0.5, y=0.38,
                    showarrow=False,
                    font=dict(size=11, color=raygun.COLORS['neon_cyan'], family='Space Mono, monospace')
                )
                fig.add_annotation(
                    text="<b>RSI (14)</b>",
                    xref="paper", yref="paper",
                    x=0.5, y=0.18,
                    showarrow=False,
                    font=dict(size=11, color=raygun.COLORS['purple_haze'], family='Space Mono, monospace')
                )

                # Habilitar zoom independiente en cada eje Y - RAYGUN GRID
                fig.update_yaxes(
                    fixedrange=False, gridcolor=raygun.COLORS['grid'],
                    linecolor=raygun.COLORS['neon_pink'], title_text='', row=1, col=1
                )
                fig.update_yaxes(
                    fixedrange=False, gridcolor=raygun.COLORS['grid'],
                    linecolor=raygun.COLORS['neon_cyan'], title_text='', row=2, col=1
                )
                fig.update_yaxes(
                    range=[0, 100], fixedrange=False, gridcolor=raygun.COLORS['grid'],
                    linecolor=raygun.COLORS['purple_haze'], title_text='', row=3, col=1
                )
                fig.update_xaxes(fixedrange=False, gridcolor=raygun.COLORS['grid'], title_text='')

                # Configurar eje X con fechas como etiquetas (velas continuas sin gaps)
                fig.update_xaxes(
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext,
                    tickangle=-45,
                    row=3, col=1  # Solo mostrar etiquetas en el último subplot
                )
                # Ocultar ticks en los otros subplots pero mantener el grid
                fig.update_xaxes(showticklabels=False, row=1, col=1)
                fig.update_xaxes(showticklabels=False, row=2, col=1)

                # Chart title as separate HTML element
                st.markdown(f"""
                <div style="
                    font-family: 'Bebas Neue', Impact, sans-serif;
                    font-size: 1.5rem;
                    color: #FF00FF;
                    letter-spacing: 0.08em;
                    margin-bottom: 5px;
                    text-shadow: 2px 2px 0 rgba(0,255,255,0.3);
                ">/// {ticker} /// {timeframe} /// {period} ///</div>
                """, unsafe_allow_html=True)

                st.plotly_chart(fig, use_container_width=True, config={
                    'scrollZoom': True,
                    'displayModeBar': True,
                    'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape']
                })

                # Métricas rápidas
                col1, col2, col3, col4 = st.columns(4)
                last_close = df['close'].iloc[-1]
                prev_close = df['close'].iloc[-2] if len(df) > 1 else last_close
                change = ((last_close - prev_close) / prev_close) * 100

                col1.metric("Último Precio", f"${last_close:.2f}", f"{change:+.2f}%")
                col2.metric(f"Máx. ({period})", f"${df['high'].max():.2f}")
                col3.metric(f"Mín. ({period})", f"${df['low'].min():.2f}")

                # Mostrar RSI actual
                if rsi_series is not None and len(rsi_series) > 0 and not pd.isna(rsi_series.iloc[-1]):
                    last_rsi = rsi_series.iloc[-1]
                    rsi_status = "Sobrecompra" if last_rsi > 70 else "Sobreventa" if last_rsi < 30 else "Neutral"
                    col4.metric("RSI (14)", f"{last_rsi:.1f}", rsi_status)
                else:
                    col4.metric("Vol. Promedio", f"{df['volume'].mean():,.0f}")

                # Tabla de Indicadores (EMAs + VWAP)
                if ema_data or (vwap_series is not None and len(vwap_series) > 0):
                    st.subheader("Valores Actuales de Indicadores")
                    indicator_values = {"Indicador": [], "Valor": [], "vs Precio": [], "Señal": []}

                    # EMAs
                    for ema_length, ema_s in ema_data.items():
                        if len(ema_s) > 0:
                            ema_val = ema_s.iloc[-1]
                            diff_pct = ((last_close - ema_val) / ema_val) * 100
                            signal = "🟢 Por encima" if last_close > ema_val else "🔴 Por debajo"
                            indicator_values["Indicador"].append(f"EMA {ema_length}")
                            indicator_values["Valor"].append(f"${ema_val:.2f}")
                            indicator_values["vs Precio"].append(f"{diff_pct:+.2f}%")
                            indicator_values["Señal"].append(signal)

                    # VWAP
                    if vwap_series is not None and len(vwap_series) > 0:
                        vwap_val = vwap_series.iloc[-1]
                        diff_pct = ((last_close - vwap_val) / vwap_val) * 100
                        signal = "🟢 Por encima" if last_close > vwap_val else "🔴 Por debajo"
                        indicator_values["Indicador"].append("VWAP")
                        indicator_values["Valor"].append(f"${vwap_val:.2f}")
                        indicator_values["vs Precio"].append(f"{diff_pct:+.2f}%")
                        indicator_values["Señal"].append(signal)

                    # Custom HTML table with Raygun styling
                    html_table = """<table style="width:100%;border-collapse:collapse;background:#0D0D0D;font-family:'Space Mono',monospace;">
                    <thead><tr style="background:#1A1A2E;border-bottom:3px solid #FF00FF;">
                    <th style="padding:12px 10px;text-align:left;color:#FF00FF;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">Indicador</th>
                    <th style="padding:12px 10px;text-align:left;color:#FF00FF;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">Valor</th>
                    <th style="padding:12px 10px;text-align:left;color:#FF00FF;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">vs Precio</th>
                    <th style="padding:12px 10px;text-align:left;color:#FF00FF;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">Señal</th>
                    </tr></thead><tbody>"""
                    for i in range(len(indicator_values["Indicador"])):
                        row_bg = "#0D0D0D" if i % 2 == 0 else "#1A1A2E"
                        html_table += f"""<tr style="background:{row_bg};border-bottom:1px solid #333;">
                        <td style="padding:10px;color:#E0E0E0;font-size:0.85rem;">{indicator_values["Indicador"][i]}</td>
                        <td style="padding:10px;color:#66E0E0;font-size:0.85rem;">{indicator_values["Valor"][i]}</td>
                        <td style="padding:10px;color:#E0E0E0;font-size:0.85rem;">{indicator_values["vs Precio"][i]}</td>
                        <td style="padding:10px;color:#E0E0E0;font-size:0.85rem;">{indicator_values["Señal"][i]}</td>
                        </tr>"""
                    html_table += "</tbody></table>"
                    st.markdown(html_table, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error al cargar precios: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# TAB 3: Opciones
with tab3:
    st.header(f"Opciones - {ticker}")

    try:
        with st.spinner("Cargando cadena de opciones..."):
            # Obtener cadena de opciones
            options = obb.derivatives.options.chains(ticker)
            df_options = options.to_dataframe()

            if not df_options.empty:
                # Filtros
                col1, col2, col3 = st.columns(3)

                with col1:
                    if 'expiration' in df_options.columns:
                        expirations = df_options['expiration'].unique()
                        selected_exp = st.selectbox("Fecha de Expiración:", sorted(expirations)[:10])
                    else:
                        selected_exp = None

                with col2:
                    option_type = st.selectbox("Tipo:", ["Todas", "call", "put"])

                with col3:
                    if 'strike' in df_options.columns:
                        min_strike = float(df_options['strike'].min())
                        max_strike = float(df_options['strike'].max())
                        st.markdown("**Rango de Strike:**")
                        strike_range = st.slider(
                            label="Rango de Strike",
                            min_value=min_strike,
                            max_value=max_strike,
                            value=(min_strike, max_strike),
                            format="$%.2f",
                            label_visibility="collapsed"
                        )
                    else:
                        strike_range = None

                # Filtrar datos
                df_filtered = df_options.copy()

                if selected_exp and 'expiration' in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered['expiration'] == selected_exp]

                if option_type != "Todas" and 'option_type' in df_filtered.columns:
                    df_filtered = df_filtered[df_filtered['option_type'] == option_type]

                if strike_range and 'strike' in df_filtered.columns:
                    df_filtered = df_filtered[
                        (df_filtered['strike'] >= strike_range[0]) &
                        (df_filtered['strike'] <= strike_range[1])
                    ]

                # Mostrar columnas relevantes
                display_cols = ['strike', 'option_type', 'expiration', 'bid', 'ask',
                               'last_price', 'volume', 'open_interest', 'implied_volatility']
                available_cols = [c for c in display_cols if c in df_filtered.columns]

                st.subheader(f"Cadena de Opciones ({len(df_filtered)} contratos)")
                # Rename columns to uppercase for display consistency
                df_display = df_filtered[available_cols].head(50).copy()
                df_display.columns = [col.upper().replace('_', ' ') for col in df_display.columns]
                st.dataframe(df_display, use_container_width=True)

                # Análisis de Open Interest - RAYGUN STYLE
                if 'open_interest' in df_filtered.columns and 'strike' in df_filtered.columns:
                    st.subheader("Open Interest por Strike")

                    oi_by_strike = df_filtered.groupby(['strike', 'option_type'])['open_interest'].sum().unstack(fill_value=0)

                    fig = go.Figure()
                    if 'call' in oi_by_strike.columns:
                        fig.add_trace(go.Bar(x=oi_by_strike.index, y=oi_by_strike['call'],
                                            name='CALLS', marker_color=raygun.COLORS['neon_green']))
                    if 'put' in oi_by_strike.columns:
                        fig.add_trace(go.Bar(x=oi_by_strike.index, y=oi_by_strike['put'],
                                            name='PUTS', marker_color=raygun.COLORS['hot_pink']))

                    fig.update_layout(
                        barmode='group',
                        paper_bgcolor=raygun.COLORS['bg_dark'],
                        plot_bgcolor=raygun.COLORS['bg_dark'],
                        font=dict(family='Space Mono', color=raygun.COLORS['text_light']),
                        xaxis_title="STRIKE", yaxis_title="OPEN INTEREST",
                        xaxis=dict(gridcolor=raygun.COLORS['grid']),
                        yaxis=dict(gridcolor=raygun.COLORS['grid'])
                    )
                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("No se encontraron datos de opciones")

    except Exception as e:
        st.error(f"Error al cargar opciones: {str(e)}")
        st.info("Algunos proveedores requieren API keys adicionales para datos de opciones")

# TAB 4: Financieros
with tab4:
    st.header(f"Estados Financieros - {ticker}")

    col1, col2 = st.columns(2)
    with col1:
        financial_type = st.selectbox("Tipo de Estado:",
                                      ["Income Statement", "Balance Sheet", "Cash Flow"])
    with col2:
        period_type = st.selectbox("Período:", ["annual", "quarter"])

    try:
        with st.spinner("Cargando datos financieros..."):
            if financial_type == "Income Statement":
                data = obb.equity.fundamental.income(ticker, period=period_type, limit=5)
            elif financial_type == "Balance Sheet":
                data = obb.equity.fundamental.balance(ticker, period=period_type, limit=5)
            else:
                data = obb.equity.fundamental.cash(ticker, period=period_type, limit=5)

            df = data.to_dataframe()

            if not df.empty:
                # Función para formatear valores financieros
                def format_financial(val):
                    if pd.isna(val):
                        return "—"
                    if isinstance(val, str):
                        return val
                    if isinstance(val, (int, float)):
                        if abs(val) >= 1e12:
                            return f"${val/1e12:.2f}T"
                        elif abs(val) >= 1e9:
                            return f"${val/1e9:.2f}B"
                        elif abs(val) >= 1e6:
                            return f"${val/1e6:.2f}M"
                        elif abs(val) >= 1e3:
                            return f"${val/1e3:.2f}K"
                        else:
                            return f"${val:,.2f}"
                    return str(val)

                # Obtener fechas para las columnas
                if 'period_ending' in df.columns:
                    dates = [str(d)[:10] for d in df['period_ending']]
                else:
                    dates = [f"Period {i+1}" for i in range(len(df))]

                # Seleccionar columnas numéricas relevantes
                exclude_cols = ['period_ending', 'fiscal_period', 'fiscal_year', 'symbol']
                numeric_cols = [c for c in df.columns if c not in exclude_cols]

                # Crear tabla formateada manualmente
                formatted_data = []
                for col in numeric_cols:
                    row = {"Métrica": col.replace('_', ' ').title()}
                    for i, date in enumerate(dates):
                        val = df[col].iloc[i] if i < len(df) else None
                        row[date] = format_financial(val)
                    formatted_data.append(row)

                df_display = pd.DataFrame(formatted_data)
                st.dataframe(df_display, use_container_width=True, height=500)

                # Gráfico de métricas clave
                st.subheader("Tendencia de Métricas Clave")

                key_metrics_map = {
                    "Income Statement": ['total_revenue', 'gross_profit', 'net_income', 'operating_income', 'ebitda'],
                    "Balance Sheet": ['total_assets', 'total_liabilities', 'total_equity', 'cash_and_equivalents', 'total_debt'],
                    "Cash Flow": ['operating_cash_flow', 'capital_expenditure', 'free_cash_flow']
                }

                available_metrics = [m for m in key_metrics_map[financial_type] if m in df.columns]

                if available_metrics:
                    selected_metric = st.selectbox("Selecciona métrica para graficar:", available_metrics)

                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=dates,
                        y=df[selected_metric].values,
                        name=selected_metric.replace('_', ' ').upper(),
                        marker_color=raygun.COLORS['neon_cyan'],
                        marker_line_color=raygun.COLORS['neon_pink'],
                        marker_line_width=2
                    ))
                    fig.update_layout(
                        paper_bgcolor=raygun.COLORS['bg_dark'],
                        plot_bgcolor=raygun.COLORS['bg_dark'],
                        font=dict(family='Space Mono', color=raygun.COLORS['text_light']),
                        xaxis_title="PERIODO",
                        yaxis_title="USD",
                        height=400,
                        xaxis=dict(gridcolor=raygun.COLORS['grid']),
                        yaxis=dict(gridcolor=raygun.COLORS['grid'])
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No se encontraron datos financieros")

    except Exception as e:
        st.error(f"Error al cargar financieros: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# TAB 5: Análisis (Analyst Targets, Key Metrics, Insider Trading)
with tab5:
    st.header(f"Análisis - {ticker}")

    analysis_tabs = st.tabs(["🎯 Price Targets", "📊 Key Metrics", "👔 Insider Trading"])

    # Sub-tab 1: Analyst Price Targets (usando yfinance - gratis)
    with analysis_tabs[0]:
        st.subheader("Price Targets de Analistas")
        try:
            with st.spinner("Cargando price targets..."):
                import yfinance as yf
                yf_ticker = yf.Ticker(ticker)
                pt_data = yf_ticker.analyst_price_targets
                recommendations = yf_ticker.recommendations

                if pt_data:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Target Promedio", f"${pt_data.get('mean', 0):.2f}")
                    col2.metric("Target Máximo", f"${pt_data.get('high', 0):.2f}")
                    col3.metric("Target Mínimo", f"${pt_data.get('low', 0):.2f}")
                    col4.metric("Precio Actual", f"${pt_data.get('current', 0):.2f}")

                    # Visualización de rango de targets
                    st.markdown("---")
                    st.subheader("Rango de Price Targets")
                    fig = go.Figure()
                    fig.add_trace(go.Indicator(
                        mode="gauge+number+delta",
                        value=pt_data.get('current', 0),
                        delta={'reference': pt_data.get('mean', 0), 'relative': True, 'valueformat': '.1%'},
                        gauge={
                            'axis': {'range': [pt_data.get('low', 0) * 0.9, pt_data.get('high', 0) * 1.1]},
                            'bar': {'color': raygun.COLORS['neon_cyan']},
                            'bgcolor': raygun.COLORS['bg_card'],
                            'steps': [
                                {'range': [pt_data.get('low', 0), pt_data.get('mean', 0)], 'color': raygun.COLORS['neon_pink']},
                                {'range': [pt_data.get('mean', 0), pt_data.get('high', 0)], 'color': raygun.COLORS['neon_green']}
                            ],
                            'threshold': {
                                'line': {'color': raygun.COLORS['text_light'], 'width': 4},
                                'thickness': 0.75,
                                'value': pt_data.get('median', pt_data.get('mean', 0))
                            }
                        },
                        title={'text': "Precio vs Targets", 'font': {'color': raygun.COLORS['text_light']}}
                    ))
                    fig.update_layout(
                        paper_bgcolor=raygun.COLORS['bg_dark'],
                        font=dict(family='Space Mono', color=raygun.COLORS['text_light']),
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Upside/Downside
                    current = pt_data.get('current', 0)
                    mean_target = pt_data.get('mean', 0)
                    if current > 0 and mean_target > 0:
                        upside = ((mean_target - current) / current) * 100
                        st.metric("Upside/Downside al Target Promedio", f"{upside:+.1f}%")

                # Recomendaciones detalladas de analistas e instituciones
                upgrades_downgrades = yf_ticker.upgrades_downgrades
                if upgrades_downgrades is not None and not upgrades_downgrades.empty:
                    st.markdown("---")
                    st.subheader("Recomendaciones de Analistas e Instituciones")

                    # Preparar datos
                    df_ud = upgrades_downgrades.head(25).reset_index()
                    df_ud.columns = ['Fecha', 'Institución', 'Recomendación', 'Rec. Anterior',
                                    'Acción', 'Cambio Target', 'Target Actual', 'Target Anterior']

                    # Formatear fecha
                    df_ud['Fecha'] = pd.to_datetime(df_ud['Fecha']).dt.strftime('%Y-%m-%d')

                    # Formatear targets como moneda
                    df_ud['Target Actual'] = df_ud['Target Actual'].apply(
                        lambda x: f"${x:.0f}" if pd.notna(x) else "—")
                    df_ud['Target Anterior'] = df_ud['Target Anterior'].apply(
                        lambda x: f"${x:.0f}" if pd.notna(x) else "—")

                    # Mapear acciones a español
                    action_map = {'up': '⬆️ Upgrade', 'down': '⬇️ Downgrade',
                                 'main': '➡️ Mantiene', 'reit': '🔄 Reitera', 'init': '🆕 Inicia'}
                    df_ud['Acción'] = df_ud['Acción'].map(action_map).fillna(df_ud['Acción'])

                    # Mapear cambios de target
                    target_map = {'Raises': '📈 Sube', 'Lowers': '📉 Baja',
                                 'Maintains': '➡️ Mantiene', 'Initiates': '🆕 Inicia'}
                    df_ud['Cambio Target'] = df_ud['Cambio Target'].map(target_map).fillna(df_ud['Cambio Target'])

                    st.dataframe(df_ud, use_container_width=True, hide_index=True)

                    # Resumen de recomendaciones actuales
                    st.markdown("---")
                    st.subheader("Resumen de Consenso")
                    if recommendations is not None and not recommendations.empty:
                        latest = recommendations.iloc[0]
                        col1, col2, col3, col4, col5 = st.columns(5)
                        col1.metric("Strong Buy", int(latest.get('strongBuy', 0)))
                        col2.metric("Buy", int(latest.get('buy', 0)))
                        col3.metric("Hold", int(latest.get('hold', 0)))
                        col4.metric("Sell", int(latest.get('sell', 0)))
                        col5.metric("Strong Sell", int(latest.get('strongSell', 0)))

                        # Gráfico de barras del consenso
                        fig_consensus = go.Figure()
                        categories = ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']
                        values = [latest.get('strongBuy', 0), latest.get('buy', 0),
                                 latest.get('hold', 0), latest.get('sell', 0), latest.get('strongSell', 0)]
                        colors = [raygun.COLORS['neon_green'], '#7CFC00', raygun.COLORS['electric_yellow'],
                                 '#FF6347', raygun.COLORS['neon_pink']]
                        fig_consensus.add_trace(go.Bar(
                            x=categories, y=values,
                            marker_color=colors,
                            text=values, textposition='auto'
                        ))
                        fig_consensus.update_layout(
                            paper_bgcolor=raygun.COLORS['bg_dark'],
                            plot_bgcolor=raygun.COLORS['bg_dark'],
                            font=dict(family='Space Mono', color=raygun.COLORS['text_light']),
                            height=300,
                            xaxis=dict(gridcolor=raygun.COLORS['grid']),
                            yaxis=dict(gridcolor=raygun.COLORS['grid'], title="# Analistas")
                        )
                        st.plotly_chart(fig_consensus, use_container_width=True)
                elif not pt_data:
                    st.info("No hay price targets disponibles para este ticker")
        except Exception as e:
            st.error(f"Error al cargar price targets: {str(e)}")

    # Sub-tab 2: Key Metrics
    with analysis_tabs[1]:
        st.subheader("Métricas Clave de Valoración")
        try:
            with st.spinner("Cargando métricas..."):
                metrics_data = obb.equity.fundamental.metrics(ticker)
                df_metrics = metrics_data.to_dataframe()

                if not df_metrics.empty:
                    # Organizar métricas en columnas
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown("### 📈 Valoración")
                        valuation_metrics = [
                            ('pe_ratio', 'P/E Ratio'),
                            ('foward_pe', 'Forward P/E'),
                            ('price_to_sales', 'Price/Sales'),
                            ('price_to_book', 'Price/Book'),
                            ('peg_ratio', 'PEG Ratio'),
                            ('ev_to_ebitda', 'EV/EBITDA')
                        ]
                        for field, label in valuation_metrics:
                            if field in df_metrics.columns:
                                val = df_metrics[field].iloc[0]
                                if pd.notna(val):
                                    st.write(f"**{label}:** {val:.2f}")

                    with col2:
                        st.markdown("### 💰 Por Acción")
                        per_share_metrics = [
                            ('eps', 'EPS'),
                            ('book_value_per_share', 'Book Value/Share'),
                            ('cash_per_share', 'Cash/Share'),
                            ('revenue_per_share', 'Revenue/Share'),
                            ('free_cash_flow_per_share', 'FCF/Share'),
                            ('tangible_book_value_per_share', 'Tangible Book/Share')
                        ]
                        for field, label in per_share_metrics:
                            if field in df_metrics.columns:
                                val = df_metrics[field].iloc[0]
                                if pd.notna(val):
                                    st.write(f"**{label}:** ${val:.2f}")

                    with col3:
                        st.markdown("### 📊 Rentabilidad")
                        profitability_metrics = [
                            ('return_on_equity', 'ROE'),
                            ('return_on_assets', 'ROA'),
                            ('return_on_capital_employed', 'ROCE'),
                            ('gross_profit_margin', 'Margen Bruto'),
                            ('operating_profit_margin', 'Margen Operativo'),
                            ('net_profit_margin', 'Margen Neto')
                        ]
                        for field, label in profitability_metrics:
                            if field in df_metrics.columns:
                                val = df_metrics[field].iloc[0]
                                if pd.notna(val):
                                    if 'margin' in field or 'return' in field:
                                        st.write(f"**{label}:** {val*100:.2f}%")
                                    else:
                                        st.write(f"**{label}:** {val:.2f}")

                    # Más métricas
                    st.markdown("---")
                    col4, col5 = st.columns(2)

                    with col4:
                        st.markdown("### 🏦 Deuda y Liquidez")
                        debt_metrics = [
                            ('debt_to_equity', 'Debt/Equity'),
                            ('debt_to_assets', 'Debt/Assets'),
                            ('current_ratio', 'Current Ratio'),
                            ('quick_ratio', 'Quick Ratio'),
                            ('interest_coverage', 'Interest Coverage')
                        ]
                        for field, label in debt_metrics:
                            if field in df_metrics.columns:
                                val = df_metrics[field].iloc[0]
                                if pd.notna(val):
                                    st.write(f"**{label}:** {val:.2f}")

                    with col5:
                        st.markdown("### 📉 Dividendos")
                        div_metrics = [
                            ('dividend_yield', 'Dividend Yield'),
                            ('payout_ratio', 'Payout Ratio'),
                            ('dividend_per_share', 'Dividend/Share')
                        ]
                        for field, label in div_metrics:
                            if field in df_metrics.columns:
                                val = df_metrics[field].iloc[0]
                                if pd.notna(val):
                                    if 'yield' in field or 'ratio' in field.lower():
                                        st.write(f"**{label}:** {val*100:.2f}%")
                                    else:
                                        st.write(f"**{label}:** ${val:.2f}")
                else:
                    st.info("No hay métricas disponibles para este ticker")
        except Exception as e:
            st.error(f"Error al cargar métricas: {str(e)}")

    # Sub-tab 3: Insider Trading
    with analysis_tabs[2]:
        st.subheader("Transacciones de Insiders")
        try:
            with st.spinner("Cargando insider trading..."):
                insider_data = obb.equity.ownership.insider_trading(ticker)
                df_insider = insider_data.to_dataframe()

                if not df_insider.empty:
                    # Resumen de actividad
                    col1, col2, col3 = st.columns(3)

                    # Contar compras vs ventas
                    if 'acquisition_or_disposition' in df_insider.columns:
                        buys = len(df_insider[df_insider['acquisition_or_disposition'].str.lower().str.startswith('a')])
                        sells = len(df_insider[df_insider['acquisition_or_disposition'].str.lower().str.startswith('d')])
                        col1.metric("Compras", buys)
                        col2.metric("Ventas", sells)
                        ratio = buys / sells if sells > 0 else buys
                        col3.metric("Ratio Buy/Sell", f"{ratio:.2f}")

                    st.markdown("---")

                    # Tabla de transacciones
                    display_cols = ['filing_date', 'transaction_date', 'owner_name', 'owner_title',
                                   'transaction_type', 'acquisition_or_disposition', 'securities_owned',
                                   'securities_transacted', 'transaction_price', 'value']
                    available_cols = [c for c in display_cols if c in df_insider.columns]

                    df_display = df_insider[available_cols].head(30)

                    # Formatear valores monetarios
                    if 'transaction_price' in df_display.columns:
                        df_display['transaction_price'] = df_display['transaction_price'].apply(
                            lambda x: f"${x:.2f}" if pd.notna(x) else "—")
                    if 'value' in df_display.columns:
                        df_display['value'] = df_display['value'].apply(
                            lambda x: f"${x:,.0f}" if pd.notna(x) else "—")

                    st.dataframe(df_display, use_container_width=True, hide_index=True)

                    # Gráfico de actividad por tipo
                    if 'acquisition_or_disposition' in df_insider.columns and 'transaction_date' in df_insider.columns:
                        st.subheader("Actividad de Insiders en el Tiempo")
                        df_plot = df_insider.copy()
                        df_plot['transaction_date'] = pd.to_datetime(df_plot['transaction_date'])
                        df_plot = df_plot.dropna(subset=['transaction_date'])

                        if not df_plot.empty:
                            fig = go.Figure()

                            # Compras (Acquisition) - RAYGUN
                            buys_df = df_plot[df_plot['acquisition_or_disposition'].str.lower().str.startswith('a')]
                            if not buys_df.empty:
                                fig.add_trace(go.Scatter(
                                    x=buys_df['transaction_date'],
                                    y=[1] * len(buys_df),
                                    mode='markers',
                                    name=f'BUYS ({len(buys_df)})',
                                    marker=dict(color=raygun.COLORS['neon_green'], size=14, symbol='triangle-up',
                                               line=dict(color=raygun.COLORS['text_light'], width=1)),
                                    hovertemplate='%{x}<br><b>BUY</b><extra></extra>'
                                ))

                            # Ventas (Disposition) - RAYGUN
                            sells_df = df_plot[df_plot['acquisition_or_disposition'].str.lower().str.startswith('d')]
                            if not sells_df.empty:
                                fig.add_trace(go.Scatter(
                                    x=sells_df['transaction_date'],
                                    y=[0] * len(sells_df),
                                    mode='markers',
                                    name=f'SELLS ({len(sells_df)})',
                                    marker=dict(color=raygun.COLORS['hot_pink'], size=14, symbol='triangle-down',
                                               line=dict(color=raygun.COLORS['text_light'], width=1)),
                                    hovertemplate='%{x}<br><b>SELL</b><extra></extra>'
                                ))

                            fig.update_layout(
                                paper_bgcolor=raygun.COLORS['bg_dark'],
                                plot_bgcolor=raygun.COLORS['bg_dark'],
                                font=dict(family='Space Mono', color=raygun.COLORS['text_light']),
                                height=350,
                                yaxis=dict(
                                    tickvals=[0, 1], ticktext=['SELL', 'BUY'], range=[-0.5, 1.5],
                                    gridcolor=raygun.COLORS['grid']
                                ),
                                xaxis=dict(gridcolor=raygun.COLORS['grid']),
                                xaxis_title="DATE",
                                showlegend=True,
                                legend=dict(
                                    orientation="h", yanchor="bottom", y=1.02,
                                    bgcolor='rgba(13,13,13,0.9)', bordercolor=raygun.COLORS['neon_pink']
                                )
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No hay fechas de transacción disponibles para graficar")
                else:
                    st.info("No hay datos de insider trading disponibles para este ticker")
        except Exception as e:
            st.error(f"Error al cargar insider trading: {str(e)}")

# TAB 6: Hedge & Correlaciones
with tab6:
    st.markdown(f'<h2 style="color:#E0E0E0;margin-bottom:5px;">Análisis de Hedge para {ticker}</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#888;font-size:0.9rem;margin-bottom:20px;">Encuentra activos no correlacionados para proteger tu posición</p>', unsafe_allow_html=True)

    # Configuración del análisis
    hedge_config_cols = st.columns([2, 1, 1])
    with hedge_config_cols[0]:
        st.markdown('<div style="color:#00FFFF;font-weight:bold;margin-bottom:5px;">Período de Análisis</div>', unsafe_allow_html=True)
    with hedge_config_cols[1]:
        hedge_period = st.selectbox(
            "Período",
            options=["6mo", "1y", "2y"],
            index=1,
            key="hedge_period",
            label_visibility="collapsed"
        )
    with hedge_config_cols[2]:
        analyze_btn = st.button("🔍 Analizar Correlaciones", key="analyze_hedge_btn", use_container_width=True)

    if analyze_btn or st.session_state.get('hedge_analyzed', False):
        st.session_state['hedge_analyzed'] = True

        with st.spinner("Calculando correlaciones..."):
            # Obtener correlaciones
            correlations_df = hedge.calculate_correlations(ticker, period=hedge_period)

            if not correlations_df.empty:
                # Dividir en 2 columnas
                hedge_col1, hedge_col2 = st.columns([1, 1])

                with hedge_col1:
                    st.markdown('''
                    <div style="background:linear-gradient(135deg,rgba(57,255,20,0.1) 0%,rgba(0,255,255,0.05) 100%);
                                border:2px solid #39FF14;padding:15px;margin-bottom:15px;">
                        <h3 style="color:#39FF14;margin:0 0 10px 0;font-family:Bebas Neue,sans-serif;">
                            🛡️ MEJORES OPCIONES DE HEDGE
                        </h3>
                        <p style="color:#888;font-size:0.8rem;margin:0;">Activos con menor correlación a tu posición</p>
                    </div>
                    ''', unsafe_allow_html=True)

                    # Top 10 mejores hedges
                    top_hedges = correlations_df.head(10)

                    for idx, row in top_hedges.iterrows():
                        score_color = hedge.get_hedge_score_color(row['hedge_score'])
                        corr_color = "#39FF14" if row['correlation'] < 0 else "#FFD700" if row['correlation'] < 0.3 else "#FF8C00"

                        st.markdown(f'''
                        <div style="background:rgba(26,26,46,0.9);border-left:4px solid {score_color};
                                    padding:12px 15px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                            <div style="flex:1;">
                                <div style="display:flex;align-items:center;gap:10px;">
                                    <span style="color:#00FFFF;font-weight:bold;font-size:1.1rem;">{row['symbol']}</span>
                                    <span style="background:{score_color}30;color:{score_color};padding:2px 8px;
                                                 font-size:0.7rem;border-radius:3px;">{row['hedge_score']}</span>
                                </div>
                                <div style="color:#E0E0E0;font-size:0.85rem;margin-top:3px;">{row['name']}</div>
                                <div style="color:#888;font-size:0.75rem;margin-top:2px;">{row['category']} • {row['description']}</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="color:{corr_color};font-size:1.3rem;font-weight:bold;font-family:Space Mono,monospace;">
                                    {row['correlation']:.2f}
                                </div>
                                <div style="color:#888;font-size:0.7rem;">correlación</div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                with hedge_col2:
                    st.markdown('''
                    <div style="background:linear-gradient(135deg,rgba(255,51,102,0.1) 0%,rgba(255,0,255,0.05) 100%);
                                border:2px solid #FF3366;padding:15px;margin-bottom:15px;">
                        <h3 style="color:#FF3366;margin:0 0 10px 0;font-family:Bebas Neue,sans-serif;">
                            ⚠️ EVITAR COMO HEDGE
                        </h3>
                        <p style="color:#888;font-size:0.8rem;margin:0;">Activos altamente correlacionados (no diversifican)</p>
                    </div>
                    ''', unsafe_allow_html=True)

                    # Peores opciones (alta correlación)
                    worst_hedges = correlations_df.tail(8).iloc[::-1]

                    for idx, row in worst_hedges.iterrows():
                        score_color = hedge.get_hedge_score_color(row['hedge_score'])

                        st.markdown(f'''
                        <div style="background:rgba(26,26,46,0.9);border-left:4px solid #FF3366;
                                    padding:10px 15px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                            <div style="flex:1;">
                                <div style="color:#FF8C00;font-weight:bold;">{row['symbol']}</div>
                                <div style="color:#888;font-size:0.75rem;">{row['name']}</div>
                            </div>
                            <div style="color:#FF3366;font-size:1.1rem;font-weight:bold;font-family:Space Mono,monospace;">
                                {row['correlation']:.2f}
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                    # Matriz de correlación visual por categoría
                    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
                    st.markdown('''
                    <div style="background:rgba(0,255,255,0.05);border:1px solid #00FFFF;padding:15px;">
                        <h4 style="color:#00FFFF;margin:0 0 10px 0;">📊 Correlación por Categoría</h4>
                    </div>
                    ''', unsafe_allow_html=True)

                    # Promedio de correlación por categoría
                    category_corr = correlations_df.groupby('category')['correlation'].mean().sort_values()

                    for cat, corr in category_corr.items():
                        bar_width = min(abs(corr) * 100, 100)
                        bar_color = "#39FF14" if corr < 0 else "#FFD700" if corr < 0.3 else "#FF8C00" if corr < 0.6 else "#FF3366"

                        st.markdown(f'''
                        <div style="margin-bottom:8px;">
                            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                                <span style="color:#E0E0E0;font-size:0.8rem;">{cat}</span>
                                <span style="color:{bar_color};font-size:0.8rem;font-weight:bold;">{corr:.2f}</span>
                            </div>
                            <div style="background:rgba(255,255,255,0.1);height:8px;border-radius:4px;overflow:hidden;">
                                <div style="background:{bar_color};width:{bar_width}%;height:100%;"></div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                # Sección de análisis AI
                st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
                st.markdown('''
                <div style="background:linear-gradient(135deg,rgba(255,0,255,0.1) 0%,rgba(0,255,255,0.1) 100%);
                            border:2px solid #FF00FF;padding:20px;">
                    <h3 style="color:#FF00FF;margin:0 0 15px 0;font-family:Bebas Neue,sans-serif;display:flex;align-items:center;gap:10px;">
                        🤖 ANÁLISIS INTELIGENTE DE HEDGE
                    </h3>
                </div>
                ''', unsafe_allow_html=True)

                # Obtener info del ticker para el análisis
                try:
                    import yfinance as yf
                    ticker_yf = yf.Ticker(ticker)
                    ticker_info = ticker_yf.info
                except:
                    ticker_info = {}

                # Verificar si hay API key de Anthropic
                import os
                anthropic_key = os.getenv('ANTHROPIC_API_KEY')

                # Generar análisis
                ai_analysis = hedge.get_ai_hedge_analysis(
                    ticker=ticker,
                    correlations_df=correlations_df,
                    ticker_info=ticker_info,
                    api_key=anthropic_key
                )

                st.markdown(f'''
                <div style="background:rgba(26,26,46,0.95);padding:20px;border-left:4px solid #00FFFF;margin-top:10px;">
                    <div style="color:#E0E0E0;font-size:0.95rem;line-height:1.6;white-space:pre-wrap;">{ai_analysis}</div>
                </div>
                ''', unsafe_allow_html=True)

                # Simulador de hedge
                st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
                st.markdown('''
                <div style="background:linear-gradient(135deg,rgba(0,255,255,0.1) 0%,rgba(57,255,20,0.05) 100%);
                            border:2px solid #00FFFF;padding:20px;">
                    <h3 style="color:#00FFFF;margin:0 0 15px 0;font-family:Bebas Neue,sans-serif;">
                        📐 SIMULADOR DE HEDGE
                    </h3>
                    <p style="color:#888;font-size:0.85rem;margin:0;">Calcula el impacto de agregar un hedge a tu portafolio</p>
                </div>
                ''', unsafe_allow_html=True)

                sim_cols = st.columns([2, 1, 1])
                with sim_cols[0]:
                    hedge_options = correlations_df.head(15)['symbol'].tolist()
                    selected_hedge = st.selectbox(
                        "Selecciona activo de hedge",
                        options=hedge_options,
                        key="sim_hedge_select"
                    )
                with sim_cols[1]:
                    hedge_allocation = st.slider(
                        "% del portafolio",
                        min_value=5,
                        max_value=50,
                        value=20,
                        step=5,
                        key="sim_hedge_alloc"
                    )
                with sim_cols[2]:
                    simulate_btn = st.button("📊 Simular", key="sim_hedge_btn", use_container_width=True)

                if simulate_btn and selected_hedge:
                    with st.spinner("Simulando portafolio..."):
                        sim_results = hedge.analyze_portfolio_hedge(
                            ticker=ticker,
                            hedge_symbol=selected_hedge,
                            allocation_pct=hedge_allocation,
                            period=hedge_period
                        )

                        if sim_results:
                            sim_result_cols = st.columns(4)

                            with sim_result_cols[0]:
                                vol_change = sim_results['volatility_reduction']
                                vol_color = "#39FF14" if vol_change > 0 else "#FF3366"
                                st.markdown(f'''
                                <div style="background:rgba(26,26,46,0.9);border:1px solid {vol_color};padding:15px;text-align:center;">
                                    <div style="color:#888;font-size:0.75rem;">REDUCCIÓN VOLATILIDAD</div>
                                    <div style="color:{vol_color};font-size:1.5rem;font-weight:bold;">{vol_change:.1f}%</div>
                                </div>
                                ''', unsafe_allow_html=True)

                            with sim_result_cols[1]:
                                st.markdown(f'''
                                <div style="background:rgba(26,26,46,0.9);border:1px solid #00FFFF;padding:15px;text-align:center;">
                                    <div style="color:#888;font-size:0.75rem;">VOL. ORIGINAL</div>
                                    <div style="color:#FF8C00;font-size:1.3rem;font-weight:bold;">{sim_results['original_volatility']:.1f}%</div>
                                </div>
                                ''', unsafe_allow_html=True)

                            with sim_result_cols[2]:
                                st.markdown(f'''
                                <div style="background:rgba(26,26,46,0.9);border:1px solid #00FFFF;padding:15px;text-align:center;">
                                    <div style="color:#888;font-size:0.75rem;">VOL. CON HEDGE</div>
                                    <div style="color:#39FF14;font-size:1.3rem;font-weight:bold;">{sim_results['hedged_volatility']:.1f}%</div>
                                </div>
                                ''', unsafe_allow_html=True)

                            with sim_result_cols[3]:
                                sharpe_change = sim_results['hedged_sharpe'] - sim_results['original_sharpe']
                                sharpe_color = "#39FF14" if sharpe_change > 0 else "#FF3366"
                                st.markdown(f'''
                                <div style="background:rgba(26,26,46,0.9);border:1px solid {sharpe_color};padding:15px;text-align:center;">
                                    <div style="color:#888;font-size:0.75rem;">SHARPE RATIO</div>
                                    <div style="color:{sharpe_color};font-size:1.3rem;font-weight:bold;">{sim_results['hedged_sharpe']:.2f}</div>
                                    <div style="color:#888;font-size:0.7rem;">({'+' if sharpe_change >= 0 else ''}{sharpe_change:.2f} vs original)</div>
                                </div>
                                ''', unsafe_allow_html=True)
                        else:
                            st.warning("No se pudo simular el portafolio. Verifica que los tickers sean válidos.")

            else:
                st.warning(f"No se pudieron calcular correlaciones para {ticker}. Verifica que el ticker sea válido.")

    else:
        # Mostrar mensaje inicial
        st.markdown('''
        <div style="background:rgba(26,26,46,0.8);border:2px dashed #00FFFF;padding:40px;text-align:center;margin-top:20px;">
            <div style="font-size:3rem;margin-bottom:15px;">🛡️</div>
            <h3 style="color:#00FFFF;margin:0 0 10px 0;">Análisis de Activos No Correlacionados</h3>
            <p style="color:#888;max-width:500px;margin:0 auto;">
                Haz clic en <strong style="color:#39FF14;">"Analizar Correlaciones"</strong> para encontrar activos que pueden servir como hedge
                para tu posición en <strong style="color:#FF00FF;">{ticker}</strong>.
            </p>
            <div style="margin-top:20px;color:#666;font-size:0.8rem;">
                Analizamos correlaciones con ETFs inversos, metales preciosos, bonos, commodities, divisas y más.
            </div>
        </div>
        '''.format(ticker=ticker), unsafe_allow_html=True)

# TAB 7: Fondos y ETFs
with tab7:
    st.markdown(raygun.get_section_header("BUSCADOR DE FONDOS Y ETFs", "07"), unsafe_allow_html=True)

    # Filtros en columnas
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        fund_categories = ["Todas"] + funds.get_categories()
        selected_category = st.selectbox("Categoría", fund_categories, key="fund_category")

    with filter_col2:
        issuers = ["Todos", "Vanguard", "BlackRock", "State Street", "Invesco", "Schwab", "ARK Invest"]
        selected_issuer = st.selectbox("Emisor", issuers, key="fund_issuer")

    with filter_col3:
        max_expense = st.selectbox("Expense Ratio Máx", ["Sin límite", "0.1%", "0.25%", "0.5%", "1%"], key="fund_expense")

    with filter_col4:
        min_sharpe = st.selectbox("Sharpe Mínimo", ["Sin límite", "0.5", "1.0", "1.5", "2.0"], key="fund_sharpe")

    # Botón de búsqueda
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        fund_search = st.text_input("🔍 Buscar fondo por símbolo o nombre", key="fund_search", placeholder="Ej: SPY, Vanguard, S&P 500...")
    with search_col2:
        st.write("")  # Spacer
        search_funds_btn = st.button("📦 Buscar Fondos", key="search_funds_btn", use_container_width=True)

    st.markdown(raygun.get_divider(), unsafe_allow_html=True)

    # Resultados
    if search_funds_btn or 'fund_results' in st.session_state:
        with st.spinner("Cargando datos de fondos..."):
            # Determinar símbolos a buscar
            if fund_search:
                search_results = funds.search_funds(fund_search)
                symbols_to_fetch = [f["symbol"] for f in search_results][:20]
            elif selected_category != "Todas":
                category_funds = funds.get_funds_by_category(selected_category)
                symbols_to_fetch = [f["symbol"] for f in category_funds]
            else:
                # Mostrar muestra de fondos populares
                symbols_to_fetch = ["SPY", "VOO", "QQQ", "VTI", "BND", "VEA", "VWO", "GLD", "SCHD", "XLK", "VNQ", "TLT"]

            # Obtener datos
            if symbols_to_fetch:
                fund_data = funds.fetch_multiple_funds(symbols_to_fetch)

                if not fund_data.empty:
                    # Aplicar filtros
                    expense_map = {"Sin límite": None, "0.1%": 0.001, "0.25%": 0.0025, "0.5%": 0.005, "1%": 0.01}
                    sharpe_map = {"Sin límite": None, "0.5": 0.5, "1.0": 1.0, "1.5": 1.5, "2.0": 2.0}

                    filtered_funds = funds.filter_funds(
                        fund_data,
                        category=selected_category if selected_category != "Todas" else None,
                        max_expense_ratio=expense_map.get(max_expense),
                        min_sharpe=sharpe_map.get(min_sharpe),
                        issuer=selected_issuer if selected_issuer != "Todos" else None
                    )

                    # Mostrar resultados
                    st.markdown(f'<div style="color:{raygun.get_theme()["accent_secondary"]};font-size:0.9rem;margin-bottom:15px;">Se encontraron <strong>{len(filtered_funds)}</strong> fondos</div>', unsafe_allow_html=True)

                    # Crear cards para cada fondo
                    for idx, row in filtered_funds.iterrows():
                        t = raygun.get_theme()
                        ret_color = t['positive'] if row.get('annual_return', 0) >= 0 else t['negative']
                        sharpe_color = t['positive'] if row.get('sharpe_ratio', 0) >= 1 else t['warning'] if row.get('sharpe_ratio', 0) >= 0.5 else t['negative']

                        st.markdown(f'''
                        <div style="background:{t['bg_card']};border:1px solid {t['border']};border-left:4px solid {t['accent_primary']};padding:15px;margin-bottom:12px;">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                                <div>
                                    <span style="color:{t['accent_primary']};font-weight:bold;font-size:1.2rem;">{row['symbol']}</span>
                                    <span style="color:{t['text_muted']};font-size:0.85rem;margin-left:10px;">{row.get('name', '')[:50]}</span>
                                </div>
                                <div style="text-align:right;">
                                    <div style="color:{t['text_primary']};font-size:1.1rem;font-weight:bold;">${row.get('price', 0):.2f}</div>
                                </div>
                            </div>
                            <div style="display:flex;gap:20px;margin-top:12px;flex-wrap:wrap;">
                                <div><span style="color:{t['text_muted']};font-size:0.75rem;">AUM:</span> <span style="color:{t['text_primary']};">{funds.format_aum(row.get('aum', 0))}</span></div>
                                <div><span style="color:{t['text_muted']};font-size:0.75rem;">Expense:</span> <span style="color:{t['text_primary']};">{row.get('expense_ratio', 0)*100:.2f}%</span></div>
                                <div><span style="color:{t['text_muted']};font-size:0.75rem;">Retorno Anual:</span> <span style="color:{ret_color};">{row.get('annual_return', 0):+.2f}%</span></div>
                                <div><span style="color:{t['text_muted']};font-size:0.75rem;">Sharpe:</span> <span style="color:{sharpe_color};">{row.get('sharpe_ratio', 0):.2f}</span></div>
                                <div><span style="color:{t['text_muted']};font-size:0.75rem;">Volatilidad:</span> <span style="color:{t['text_primary']};">{row.get('volatility', 0):.1f}%</span></div>
                                <div><span style="color:{t['text_muted']};font-size:0.75rem;">Beta:</span> <span style="color:{t['text_primary']};">{row.get('beta', 1.0):.2f}</span></div>
                            </div>
                            <div style="margin-top:8px;"><span style="color:{t['text_muted']};font-size:0.7rem;">Categoría:</span> <span style="color:{t['accent_secondary']};font-size:0.8rem;">{row.get('category', 'N/A')}</span></div>
                        </div>
                        ''', unsafe_allow_html=True)

                    # Sección de análisis detallado
                    st.markdown(raygun.get_divider(), unsafe_allow_html=True)
                    st.markdown(raygun.get_section_header("ANÁLISIS DETALLADO", "07b"), unsafe_allow_html=True)

                    selected_fund = st.selectbox(
                        "Selecciona un fondo para análisis detallado",
                        options=filtered_funds['symbol'].tolist() if not filtered_funds.empty else [],
                        key="fund_detail_select"
                    )

                    if selected_fund:
                        detail_col1, detail_col2 = st.columns([1, 1])

                        with detail_col1:
                            fund_detail = funds.get_fund_metrics_summary(selected_fund)

                            if "error" not in fund_detail:
                                st.markdown(f'''
                                <div style="background:{t['bg_card']};border:1px solid {t['border']};padding:20px;">
                                    <h3 style="color:{t['accent_primary']};margin:0 0 15px 0;">{fund_detail.get('name', selected_fund)}</h3>
                                    <div style="color:{t['warning']};font-size:1.5rem;margin-bottom:15px;">{fund_detail.get('rating_label', '★★★☆☆')}</div>
                                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                                        <div style="background:{t['bg_hover']};padding:10px;border-left:3px solid {t['accent_primary']};">
                                            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;">Sharpe Ratio</div>
                                            <div style="color:{t['text_primary']};font-size:1.2rem;">{fund_detail.get('sharpe_ratio', 0):.2f}</div>
                                        </div>
                                        <div style="background:{t['bg_hover']};padding:10px;border-left:3px solid {t['accent_secondary']};">
                                            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;">Beta</div>
                                            <div style="color:{t['text_primary']};font-size:1.2rem;">{fund_detail.get('beta', 1.0):.2f}</div>
                                        </div>
                                        <div style="background:{t['bg_hover']};padding:10px;border-left:3px solid {t['positive']};">
                                            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;">Retorno Anual</div>
                                            <div style="color:{t['positive'] if fund_detail.get('annual_return', 0) >= 0 else t['negative']};font-size:1.2rem;">{fund_detail.get('annual_return', 0):+.2f}%</div>
                                        </div>
                                        <div style="background:{t['bg_hover']};padding:10px;border-left:3px solid {t['negative']};">
                                            <div style="color:{t['text_muted']};font-size:0.7rem;text-transform:uppercase;">Max Drawdown</div>
                                            <div style="color:{t['negative']};font-size:1.2rem;">{fund_detail.get('max_drawdown', 0):.2f}%</div>
                                        </div>
                                    </div>
                                </div>
                                ''', unsafe_allow_html=True)

                        with detail_col2:
                            # Análisis IA
                            if st.button("🤖 Generar Análisis IA", key="fund_ai_analysis_btn"):
                                with st.spinner("Generando análisis con IA..."):
                                    import os
                                    api_key = os.getenv("ANTHROPIC_API_KEY")
                                    fund_detail = funds.get_fund_metrics_summary(selected_fund)
                                    ai_analysis = funds.get_ai_fund_analysis(fund_detail, api_key)
                                    st.session_state.fund_ai_analysis = ai_analysis

                            if 'fund_ai_analysis' in st.session_state:
                                st.markdown(f'''
                                <div style="background:{t['bg_card']};border:1px solid {t['accent_secondary']};padding:15px;max-height:400px;overflow-y:auto;">
                                    <div style="color:{t['text_primary']};font-size:0.9rem;line-height:1.6;">{st.session_state.fund_ai_analysis}</div>
                                </div>
                                ''', unsafe_allow_html=True)

                else:
                    st.warning("No se encontraron fondos con los criterios seleccionados.")
    else:
        # Estado inicial
        t = raygun.get_theme()
        st.markdown(f'''
        <div style="background:{t['bg_card']};border:2px dashed {t['accent_secondary']};padding:40px;text-align:center;margin-top:20px;">
            <div style="font-size:3rem;margin-bottom:15px;">📦</div>
            <h3 style="color:{t['accent_secondary']};margin:0 0 10px 0;">Buscador de Fondos y ETFs</h3>
            <p style="color:{t['text_muted']};max-width:500px;margin:0 auto;">
                Utiliza los filtros arriba o haz clic en <strong style="color:{t['positive']};">"Buscar Fondos"</strong> para explorar
                nuestra base de datos de ETFs y fondos.
            </p>
            <div style="margin-top:20px;color:{t['text_muted']};font-size:0.8rem;">
                Incluye métricas como Sharpe Ratio, Beta, Expense Ratio, AUM y más.
            </div>
        </div>
        ''', unsafe_allow_html=True)

# === TAB 8: PORTFOLIO BUILDER ===
with tab8:
    t = raygun.get_theme()
    st.markdown(raygun.get_section_header("💼 Portfolio Builder", "Generador de portafolios personalizados con IA"), unsafe_allow_html=True)

    # --- Input Section ---
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        st.markdown(raygun.get_metric_card_header("Perfil de Inversión"), unsafe_allow_html=True)

        risk_profiles = portfolio.get_risk_profiles()
        selected_risk = st.selectbox(
            "Perfil de Riesgo",
            options=list(risk_profiles.keys()),
            index=1,
            key="portfolio_risk_profile"
        )
        profile_info = risk_profiles[selected_risk]
        st.caption(f"📊 {profile_info['description']}")
        st.caption(f"Volatilidad objetivo: {profile_info['target_volatility']}%")

        horizons = portfolio.get_investment_horizons()
        selected_horizon = st.selectbox(
            "Horizonte de Inversión",
            options=list(horizons.keys()),
            index=1,
            key="portfolio_horizon"
        )
        horizon_info = horizons[selected_horizon]
        st.caption(f"🎯 Enfoque: {horizon_info['focus']}")

    with input_col2:
        st.markdown(raygun.get_metric_card_header("Parámetros de Inversión"), unsafe_allow_html=True)

        investment_amount = st.number_input(
            "Monto a Invertir (USD)",
            min_value=1000,
            max_value=10000000,
            value=50000,
            step=1000,
            key="portfolio_amount"
        )

        investment_goals = st.text_area(
            "Objetivos de Inversión",
            placeholder="Ej: Jubilación en 20 años, generar ingresos pasivos, crecimiento a largo plazo...",
            height=80,
            key="portfolio_goals"
        )

        investment_constraints = st.text_area(
            "Restricciones o Preferencias",
            placeholder="Ej: Sin inversión en petróleo, preferencia ESG, máximo 30% en tech...",
            height=80,
            key="portfolio_constraints"
        )

    st.markdown(raygun.get_chaos_divider(), unsafe_allow_html=True)

    # --- Templates Section ---
    st.markdown(raygun.get_subsection_header("📦 Templates de Portafolio"), unsafe_allow_html=True)

    templates = portfolio.get_portfolio_templates()
    template_cols = st.columns(4)

    for idx, (name, template) in enumerate(templates.items()):
        with template_cols[idx % 4]:
            risk_color = {
                "Conservador": t['positive'],
                "Moderado": t['warning'],
                "Agresivo": t['accent_primary'],
                "Muy Agresivo": t['negative']
            }.get(template['risk_level'], t['text_primary'])

            st.markdown(f'''
            <div style="background:{t['bg_card']};border:1px solid {t['border']};padding:12px;margin-bottom:10px;min-height:140px;">
                <div style="color:{t['accent_primary']};font-weight:bold;font-size:0.85rem;margin-bottom:5px;">{name}</div>
                <div style="color:{t['text_muted']};font-size:0.7rem;margin-bottom:8px;">{template['description']}</div>
                <div style="display:inline-block;background:{risk_color}22;color:{risk_color};padding:2px 8px;font-size:0.65rem;border:1px solid {risk_color};">{template['risk_level']}</div>
                <div style="color:{t['text_muted']};font-size:0.6rem;margin-top:8px;">{len(template['allocations'])} activos</div>
            </div>
            ''', unsafe_allow_html=True)

    selected_template = st.selectbox(
        "Seleccionar Template",
        options=["-- Generar Personalizado --"] + list(templates.keys()),
        key="portfolio_template_select"
    )

    st.markdown(raygun.get_chaos_divider(), unsafe_allow_html=True)

    # --- Generate Portfolio ---
    gen_col1, gen_col2 = st.columns([1, 1])

    with gen_col1:
        generate_with_ai = st.button("🤖 Generar con IA", key="portfolio_generate_ai", use_container_width=True)

    with gen_col2:
        use_template = st.button("📦 Usar Template", key="portfolio_use_template", use_container_width=True)

    # Generate with AI
    if generate_with_ai:
        with st.spinner("Generando portafolio con IA..."):
            import os
            api_key = os.getenv("ANTHROPIC_API_KEY")

            recommendation = portfolio.get_ai_portfolio_recommendation(
                risk_profile=selected_risk,
                horizon=selected_horizon,
                amount=investment_amount,
                goals=investment_goals or "Crecimiento general",
                constraints=investment_constraints or "Ninguna",
                api_key=api_key
            )
            st.session_state.generated_portfolio = recommendation
            st.session_state.portfolio_source = "IA"

    # Use Template
    if use_template and selected_template != "-- Generar Personalizado --":
        template_data = templates[selected_template]
        st.session_state.generated_portfolio = {
            "name": selected_template,
            "allocations": template_data["allocations"],
            "rationale": template_data["description"]
        }
        st.session_state.portfolio_source = "Template"

    # --- Display Generated Portfolio ---
    if 'generated_portfolio' in st.session_state and st.session_state.generated_portfolio:
        portfolio_data = st.session_state.generated_portfolio

        st.markdown(raygun.get_subsection_header(f"📊 Portafolio Generado ({st.session_state.get('portfolio_source', 'IA')})"), unsafe_allow_html=True)

        if "error" in portfolio_data:
            st.error(f"Error: {portfolio_data['error']}")
        else:
            display_col1, display_col2 = st.columns([1, 1])

            with display_col1:
                # Allocation Table
                allocations = portfolio_data.get('allocations', [])
                if allocations:
                    st.markdown(f'''
                    <div style="background:{t['bg_card']};border:1px solid {t['accent_primary']};padding:15px;">
                        <div style="color:{t['accent_primary']};font-weight:bold;margin-bottom:10px;">ASIGNACIÓN DE ACTIVOS</div>
                    </div>
                    ''', unsafe_allow_html=True)

                    for alloc in allocations:
                        symbol = alloc.get('symbol', 'N/A')
                        weight = alloc.get('weight', 0)
                        category = alloc.get('category', '')

                        bar_width = min(weight, 100)
                        st.markdown(f'''
                        <div style="background:{t['bg_hover']};padding:8px;margin-bottom:5px;border-left:3px solid {t['accent_primary']};">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <div>
                                    <span style="color:{t['accent_secondary']};font-weight:bold;">{symbol}</span>
                                    <span style="color:{t['text_muted']};font-size:0.7rem;margin-left:8px;">{category}</span>
                                </div>
                                <span style="color:{t['text_primary']};font-weight:bold;">{weight:.1f}%</span>
                            </div>
                            <div style="background:{t['border']};height:4px;margin-top:5px;overflow:hidden;">
                                <div style="background:{t['accent_primary']};width:{bar_width}%;height:100%;"></div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                    # Calculate Dollar Amounts
                    st.markdown(f'''
                    <div style="background:{t['bg_card']};border:1px solid {t['border']};padding:10px;margin-top:10px;">
                        <div style="color:{t['text_muted']};font-size:0.7rem;margin-bottom:5px;">DISTRIBUCIÓN EN USD (${investment_amount:,.0f})</div>
                    ''', unsafe_allow_html=True)
                    for alloc in allocations:
                        dollar_amount = investment_amount * (alloc.get('weight', 0) / 100)
                        st.markdown(f'''
                        <div style="display:flex;justify-content:space-between;padding:3px 0;">
                            <span style="color:{t['text_muted']};font-size:0.75rem;">{alloc.get('symbol', 'N/A')}</span>
                            <span style="color:{t['positive']};font-size:0.75rem;">${dollar_amount:,.0f}</span>
                        </div>
                        ''', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with display_col2:
                # Rationale
                rationale = portfolio_data.get('rationale', 'No hay análisis disponible.')
                st.markdown(f'''
                <div style="background:{t['bg_card']};border:1px solid {t['accent_secondary']};padding:15px;margin-bottom:15px;">
                    <div style="color:{t['accent_secondary']};font-weight:bold;margin-bottom:10px;">ANÁLISIS Y RECOMENDACIÓN</div>
                    <div style="color:{t['text_primary']};font-size:0.85rem;line-height:1.5;">{rationale}</div>
                </div>
                ''', unsafe_allow_html=True)

                # Calculate metrics button
                if st.button("📈 Calcular Métricas Históricas", key="portfolio_calc_metrics"):
                    with st.spinner("Calculando métricas..."):
                        metrics = portfolio.calculate_portfolio_metrics(allocations)
                        st.session_state.portfolio_metrics = metrics

                if 'portfolio_metrics' in st.session_state and st.session_state.portfolio_metrics:
                    metrics = st.session_state.portfolio_metrics
                    if "error" not in metrics:
                        st.markdown(f'''
                        <div style="background:{t['bg_card']};border:1px solid {t['positive']};padding:15px;">
                            <div style="color:{t['positive']};font-weight:bold;margin-bottom:10px;">MÉTRICAS HISTÓRICAS (1 AÑO)</div>
                            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                                <div style="background:{t['bg_hover']};padding:8px;border-left:2px solid {t['positive']};">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Retorno Anual</div>
                                    <div style="color:{t['positive'] if metrics.get('annual_return', 0) >= 0 else t['negative']};font-size:1rem;">{metrics.get('annual_return', 0):+.2f}%</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:8px;border-left:2px solid {t['warning']};">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Volatilidad</div>
                                    <div style="color:{t['warning']};font-size:1rem;">{metrics.get('volatility', 0):.2f}%</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:8px;border-left:2px solid {t['accent_primary']};">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Sharpe Ratio</div>
                                    <div style="color:{t['accent_primary']};font-size:1rem;">{metrics.get('sharpe_ratio', 0):.2f}</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:8px;border-left:2px solid {t['negative']};">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Max Drawdown</div>
                                    <div style="color:{t['negative']};font-size:1rem;">{metrics.get('max_drawdown', 0):.2f}%</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:8px;border-left:2px solid {t['accent_secondary']};">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Beta vs SPY</div>
                                    <div style="color:{t['accent_secondary']};font-size:1rem;">{metrics.get('beta', 1.0):.2f}</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:8px;border-left:2px solid {t['text_muted']};">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Retorno Total</div>
                                    <div style="color:{t['text_primary']};font-size:1rem;">{metrics.get('total_return', 0):+.2f}%</div>
                                </div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.error(f"Error calculando métricas: {metrics['error']}")

            # Backtest Section
            st.markdown(raygun.get_chaos_divider(), unsafe_allow_html=True)
            st.markdown(raygun.get_subsection_header("📉 Backtest del Portafolio"), unsafe_allow_html=True)

            bt_col1, bt_col2 = st.columns([1, 3])
            with bt_col1:
                backtest_period = st.selectbox(
                    "Período de Backtest",
                    options=["1y", "2y", "3y", "5y"],
                    index=0,
                    key="portfolio_backtest_period"
                )
                run_backtest = st.button("▶️ Ejecutar Backtest", key="portfolio_run_backtest")

            if run_backtest:
                with st.spinner("Ejecutando backtest..."):
                    allocations = portfolio_data.get('allocations', [])
                    # Convertir período string a años int
                    years_map = {"1y": 1, "2y": 2, "3y": 3, "5y": 5}
                    years = years_map.get(backtest_period, 1)
                    backtest_result = portfolio.backtest_portfolio(allocations, years=years)
                    st.session_state.portfolio_backtest = backtest_result

            if 'portfolio_backtest' in st.session_state and st.session_state.portfolio_backtest:
                bt = st.session_state.portfolio_backtest
                if "error" not in bt:
                    with bt_col2:
                        st.markdown(f'''
                        <div style="background:{t['bg_card']};border:1px solid {t['accent_primary']};padding:15px;">
                            <div style="color:{t['accent_primary']};font-weight:bold;margin-bottom:10px;">RESULTADOS DEL BACKTEST</div>
                            <div style="display:flex;gap:15px;flex-wrap:wrap;">
                                <div style="background:{t['bg_hover']};padding:10px;flex:1;min-width:120px;">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Retorno Total</div>
                                    <div style="color:{t['positive'] if bt.get('total_return', 0) >= 0 else t['negative']};font-size:1.2rem;font-weight:bold;">{bt.get('total_return', 0):+.2f}%</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:10px;flex:1;min-width:120px;">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">CAGR</div>
                                    <div style="color:{t['accent_primary']};font-size:1.2rem;font-weight:bold;">{bt.get('cagr', 0):+.2f}%</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:10px;flex:1;min-width:120px;">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Valor Final</div>
                                    <div style="color:{t['positive']};font-size:1.2rem;font-weight:bold;">${bt.get('final_value', investment_amount):,.0f}</div>
                                </div>
                                <div style="background:{t['bg_hover']};padding:10px;flex:1;min-width:120px;">
                                    <div style="color:{t['text_muted']};font-size:0.65rem;">Max Drawdown</div>
                                    <div style="color:{t['negative']};font-size:1.2rem;font-weight:bold;">{bt.get('max_drawdown', 0):.2f}%</div>
                                </div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                    # Performance Chart
                    if 'portfolio_values' in bt:
                        import plotly.graph_objects as go
                        import pandas as pd
                        values_series = pd.Series(bt['portfolio_values'])
                        # Calcular retorno porcentual desde inicio
                        returns_pct = (values_series / values_series.iloc[0] - 1) * 100
                        fig = go.Figure()
                        # Convertir hex a rgba para fillcolor
                        hex_color = t['accent_primary'].lstrip('#')
                        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                        fill_rgba = f"rgba({r},{g},{b},0.15)"

                        fig.add_trace(go.Scatter(
                            x=returns_pct.index,
                            y=returns_pct.values,
                            mode='lines',
                            name='Portfolio',
                            line=dict(color=t['accent_primary'], width=2),
                            fill='tozeroy',
                            fillcolor=fill_rgba
                        ))
                        fig.update_layout(
                            title="Rendimiento Acumulado",
                            xaxis_title="Fecha",
                            yaxis_title="Retorno (%)",
                            template="plotly_dark" if t['bg_primary'] == '#000000' else "plotly_white",
                            height=300,
                            margin=dict(l=40, r=40, t=40, b=40),
                            paper_bgcolor=t['bg_primary'],
                            plot_bgcolor=t['bg_secondary'],
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Error en backtest: {bt['error']}")

# === GLOSSARY DIALOG ===
@st.dialog("📖 GLOSARIO FINANCIERO", width="large")
def show_glossary_dialog():
    """Muestra el glosario financiero como popup flotante."""
    st.markdown("""
    <style>
    [data-testid="stDialog"] {
        background: linear-gradient(135deg, rgba(13,13,30,0.98) 0%, rgba(26,26,46,0.98) 100%) !important;
        border: 2px solid #FF00FF !important;
        box-shadow: 0 0 30px rgba(255,0,255,0.3), 0 0 60px rgba(0,255,255,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Buscar término", key="glossary_dialog_search", placeholder="Ej: RSI, P/E, MACD...")
    with col2:
        all_categories = ["Todas"] + list(GLOSSARY_TERMS.keys())
        selected_cat = st.selectbox("Categoría", all_categories, key="glossary_dialog_cat")

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,#FF00FF,#00FFFF);margin:10px 0 15px 0;"></div>', unsafe_allow_html=True)

    # Container con scroll para los términos
    terms_container = st.container(height=450)
    with terms_container:
        for category, terms in GLOSSARY_TERMS.items():
            if selected_cat != "Todas" and category != selected_cat:
                continue

            filtered_terms = terms
            if search_term:
                filtered_terms = [t for t in terms if search_term.lower() in t["term"].lower() or search_term.lower() in t["definition"].lower()]

            if filtered_terms:
                st.markdown(f'<div style="color:#FF00FF;font-weight:bold;font-size:1rem;margin:15px 0 8px 0;border-bottom:2px solid #FF00FF;padding-bottom:5px;">{category}</div>', unsafe_allow_html=True)
                for t in filtered_terms:
                    st.markdown(f'''
                    <div style="background:rgba(26,26,46,0.9);border-left:4px solid #00FFFF;padding:10px 15px;margin-bottom:10px;border-radius:0 6px 6px 0;">
                        <div style="color:#00FFFF;font-weight:bold;font-size:1rem;">{t["term"]}</div>
                        <div style="color:#E0E0E0;font-size:0.9rem;margin-top:4px;line-height:1.4;">{t["definition"]}</div>
                        <div style="color:#39FF14;font-size:0.85rem;margin-top:6px;font-style:italic;background:rgba(57,255,20,0.1);padding:6px 10px;border-radius:4px;">💡 {t["example"]}</div>
                    </div>
                    ''', unsafe_allow_html=True)

# Glossary button in sidebar
st.sidebar.markdown(raygun.get_sidebar_section("Reference"), unsafe_allow_html=True)
if st.sidebar.button("📖 GLOSARIO FINANCIERO", key="open_glossary_btn", use_container_width=True):
    show_glossary_dialog()

# Footer - RAYGUN STYLE
st.sidebar.markdown(raygun.get_chaos_divider(), unsafe_allow_html=True)
st.sidebar.markdown("""<div style="text-align:center;position:relative;"><p style="font-family:Space Mono,monospace;font-size:0.6rem;letter-spacing:0.25em;color:#666;text-transform:uppercase;margin-bottom:5px;">/// POWERED BY ///</p><p style="font-family:Bebas Neue,Impact,sans-serif;font-size:1.6rem;letter-spacing:0.08em;color:#FF00FF;text-shadow:2px 2px 0 #00FFFF,0 0 15px rgba(255,0,255,0.3);margin:0;transform:rotate(-1deg);display:inline-block;">OPENBB</p><p style="font-family:Space Mono,monospace;font-size:0.5rem;color:#555;margin-top:8px;letter-spacing:0.15em;">[<a href="https://docs.openbb.co" style="color:#00FFFF;text-decoration:none;">DOCS</a>] [<a href="https://openbb.co" style="color:#39FF14;text-decoration:none;">WEB</a>]</p></div>""", unsafe_allow_html=True)
