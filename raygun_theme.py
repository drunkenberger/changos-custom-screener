"""
RAYGUN THEME - Plotly Template & Color System
Multi-theme support: Raygun, Dark, Light, Corporate
"""

import plotly.graph_objects as go
import plotly.io as pio

# === THEME PALETTES ===

# Raygun Theme (Original - David Carson inspired)
THEME_RAYGUN = {
    'name': 'Raygun',
    'bg_primary': '#0D0D0D',
    'bg_secondary': '#1A1A2E',
    'bg_card': '#1A1A2E',
    'bg_hover': '#2A2A4E',
    'accent_primary': '#FF00FF',
    'accent_secondary': '#00FFFF',
    'accent_tertiary': '#39FF14',
    'text_primary': '#FFFFFF',
    'text_secondary': '#E0E0E0',
    'text_muted': '#888888',
    'border': '#FF00FF',
    'grid': '#333333',
    'candle_up': '#39FF14',
    'candle_down': '#FF3366',
    'positive': '#39FF14',
    'negative': '#FF3366',
    'warning': '#FFE600',
    'font_title': 'Bebas Neue, Impact, sans-serif',
    'font_body': 'Space Mono, Consolas, monospace',
    'style': 'chaotic'  # For conditional styling
}

# Dark Theme (Clean, modern dark)
THEME_DARK = {
    'name': 'Dark',
    'bg_primary': '#1a1a1a',
    'bg_secondary': '#242424',
    'bg_card': '#2d2d2d',
    'bg_hover': '#3d3d3d',
    'accent_primary': '#3b82f6',
    'accent_secondary': '#60a5fa',
    'accent_tertiary': '#22c55e',
    'text_primary': '#ffffff',
    'text_secondary': '#e5e5e5',
    'text_muted': '#a3a3a3',
    'border': '#404040',
    'grid': '#333333',
    'candle_up': '#22c55e',
    'candle_down': '#ef4444',
    'positive': '#22c55e',
    'negative': '#ef4444',
    'warning': '#f59e0b',
    'font_title': 'Inter, -apple-system, sans-serif',
    'font_body': 'Inter, -apple-system, sans-serif',
    'style': 'clean'
}

# Light Theme (Clean, professional light)
THEME_LIGHT = {
    'name': 'Light',
    'bg_primary': '#ffffff',
    'bg_secondary': '#f5f5f5',
    'bg_card': '#ffffff',
    'bg_hover': '#e5e5e5',
    'accent_primary': '#2563eb',
    'accent_secondary': '#3b82f6',
    'accent_tertiary': '#16a34a',
    'text_primary': '#171717',
    'text_secondary': '#404040',
    'text_muted': '#737373',
    'border': '#e5e5e5',
    'grid': '#e5e5e5',
    'candle_up': '#16a34a',
    'candle_down': '#dc2626',
    'positive': '#16a34a',
    'negative': '#dc2626',
    'warning': '#d97706',
    'font_title': 'Inter, -apple-system, sans-serif',
    'font_body': 'Inter, -apple-system, sans-serif',
    'style': 'clean'
}

# Corporate Theme (Bloomberg Terminal / JP Morgan inspired)
THEME_CORPORATE = {
    'name': 'Corporate',
    'bg_primary': '#000000',        # Pure black like Bloomberg
    'bg_secondary': '#0d1117',      # Slightly lighter black
    'bg_card': '#161b22',           # Card background
    'bg_hover': '#21262d',          # Hover state
    'accent_primary': '#ff6600',    # Bloomberg orange
    'accent_secondary': '#58a6ff',  # Professional blue
    'accent_tertiary': '#3fb950',   # Success green
    'text_primary': '#f0f6fc',      # Bright white text
    'text_secondary': '#c9d1d9',    # Secondary text
    'text_muted': '#8b949e',        # Muted text
    'border': '#30363d',            # Subtle borders
    'grid': '#21262d',              # Grid lines
    'candle_up': '#3fb950',         # Green for up
    'candle_down': '#f85149',       # Red for down
    'positive': '#3fb950',
    'negative': '#f85149',
    'warning': '#d29922',
    'font_title': '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
    'font_body': 'SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace',
    'style': 'corporate'
}

# Theme registry
THEMES = {
    'Raygun': THEME_RAYGUN,
    'Dark': THEME_DARK,
    'Light': THEME_LIGHT,
    'Corporate': THEME_CORPORATE
}

# Current theme (default to Raygun)
_current_theme = 'Raygun'

def set_theme(theme_name: str):
    """Set the current theme."""
    global _current_theme
    if theme_name in THEMES:
        _current_theme = theme_name

def get_theme():
    """Get the current theme dictionary."""
    return THEMES.get(_current_theme, THEME_RAYGUN)

def get_theme_name():
    """Get the current theme name."""
    return _current_theme

# Legacy COLORS dict - maps to current theme for backwards compatibility
def get_colors():
    """Get colors for current theme (backwards compatible)."""
    t = get_theme()
    return {
        'bg_dark': t['bg_primary'],
        'bg_card': t['bg_card'],
        'bg_hover': t['bg_hover'],
        'neon_pink': t['accent_primary'],
        'neon_cyan': t['accent_secondary'],
        'neon_green': t['accent_tertiary'],
        'hot_pink': t['negative'],
        'electric_yellow': t['warning'],
        'grunge_orange': t['warning'],
        'purple_haze': t['accent_primary'],
        'text_light': t['text_primary'],
        'text_muted': t['text_muted'],
        'grid': t['grid'],
        'candle_up': t['candle_up'],
        'candle_down': t['candle_down'],
        'volume_up': t['candle_up'],
        'volume_down': t['candle_down'],
    }

# For backwards compatibility
COLORS = {
    'bg_dark': '#0D0D0D',
    'bg_card': '#1A1A2E',
    'bg_hover': '#2A2A4E',
    'neon_pink': '#FF00FF',
    'neon_cyan': '#00FFFF',
    'neon_green': '#39FF14',
    'hot_pink': '#FF3366',
    'electric_yellow': '#FFE600',
    'grunge_orange': '#FF6B35',
    'purple_haze': '#9B59B6',
    'text_light': '#FFFFFF',
    'text_muted': '#888888',
    'grid': '#333333',
    'candle_up': '#39FF14',
    'candle_down': '#FF3366',
    'volume_up': '#39FF14',
    'volume_down': '#FF3366',
}

# === EMA COLORS by theme ===
EMA_COLORS_BY_THEME = {
    'Raygun': {20: '#FFE600', 50: '#00FFFF', 100: '#FF00FF', 200: '#39FF14'},
    'Dark': {20: '#f59e0b', 50: '#3b82f6', 100: '#8b5cf6', 200: '#22c55e'},
    'Light': {20: '#d97706', 50: '#2563eb', 100: '#7c3aed', 200: '#16a34a'},
    'Corporate': {20: '#f7931a', 50: '#4a90d9', 100: '#7e57c2', 200: '#26a69a'},
}

def get_ema_colors():
    """Get EMA colors for current theme."""
    return EMA_COLORS_BY_THEME.get(_current_theme, EMA_COLORS_BY_THEME['Raygun'])

# Legacy EMA_COLORS for backwards compatibility
EMA_COLORS = EMA_COLORS_BY_THEME['Raygun']


def create_plotly_template(theme_name: str = None):
    """Create a Plotly template for the specified theme."""
    t = THEMES.get(theme_name, get_theme()) if theme_name else get_theme()

    return go.layout.Template(
        layout=go.Layout(
            paper_bgcolor=t['bg_primary'],
            plot_bgcolor=t['bg_primary'],
            font=dict(
                family=t['font_body'],
                color=t['text_primary'],
                size=11
            ),
            title=dict(
                font=dict(
                    family=t['font_title'],
                    size=24 if t['style'] == 'corporate' else 28,
                    color=t['accent_primary']
                ),
                x=0.02,
                xanchor='left',
                y=0.98,
                yanchor='top'
            ),
            xaxis=dict(
                gridcolor=t['grid'],
                gridwidth=1,
                zerolinecolor=t['accent_primary'],
                zerolinewidth=1 if t['style'] == 'corporate' else 2,
                linecolor=t['border'],
                linewidth=1,
                tickfont=dict(family=t['font_body'], size=9, color=t['text_muted']),
            ),
            yaxis=dict(
                gridcolor=t['grid'],
                gridwidth=1,
                zerolinecolor=t['accent_secondary'],
                zerolinewidth=1 if t['style'] == 'corporate' else 2,
                linecolor=t['border'],
                linewidth=1,
                tickfont=dict(family=t['font_body'], size=9, color=t['text_muted']),
            ),
            legend=dict(
                bgcolor=f"rgba({int(t['bg_card'][1:3], 16)}, {int(t['bg_card'][3:5], 16)}, {int(t['bg_card'][5:7], 16)}, 0.9)",
                bordercolor=t['border'],
                borderwidth=1,
                font=dict(family=t['font_body'], size=10, color=t['text_primary']),
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            colorway=[t['accent_primary'], t['accent_secondary'], t['accent_tertiary'],
                      t['positive'], t['negative'], t['warning']],
            hoverlabel=dict(
                bgcolor=t['bg_card'],
                bordercolor=t['border'],
                font=dict(family=t['font_body'], size=12, color=t['text_primary'])
            ),
        )
    )


def get_dynamic_streamlit_css(theme_name: str = None):
    """Generate dynamic CSS for Streamlit based on theme."""
    t = THEMES.get(theme_name, get_theme()) if theme_name else get_theme()

    # Corporate theme has subtle, elegant styling
    if t['style'] == 'corporate':
        glow = 'none'
        border_style = 'solid'
        transform = 'none'
        title_shadow = 'none'
    elif t['style'] == 'chaotic':
        glow = f'0 0 20px {t["accent_primary"]}40'
        border_style = 'solid'
        transform = 'skewX(-1deg)'
        title_shadow = f'2px 2px 0 {t["accent_secondary"]}, 0 0 20px {t["accent_primary"]}60'
    else:
        glow = 'none'
        border_style = 'solid'
        transform = 'none'
        title_shadow = 'none'

    return f"""
    <style>
    /* === THEME: {t['name']} === */

    /* Main background */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {t['bg_primary']} !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {t['bg_secondary']} !important;
        border-right: 1px solid {t['border']} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {t['text_primary']} !important;
    }}

    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {t['text_primary']} !important;
        font-family: {t['font_title']} !important;
    }}

    /* Text */
    p, span, div, label {{
        color: {t['text_secondary']} !important;
        font-family: {t['font_body']} !important;
    }}

    /* Cards and containers */
    [data-testid="stMetric"], .stMetric {{
        background-color: {t['bg_card']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: {'4px' if t['style'] == 'corporate' else '0px'} !important;
        padding: 1rem !important;
        box-shadow: {glow} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {t['accent_primary']} !important;
        font-family: {t['font_title']} !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {t['text_muted']} !important;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: {t['bg_card']} !important;
        color: {t['accent_primary']} !important;
        border: 1px solid {t['accent_primary']} !important;
        border-radius: {'4px' if t['style'] == 'corporate' else '0px'} !important;
        font-family: {t['font_body']} !important;
        transition: all 0.2s ease !important;
    }}

    .stButton > button:hover {{
        background-color: {t['accent_primary']}20 !important;
        box-shadow: {glow} !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {{
        background-color: {t['bg_card']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: {'4px' if t['style'] == 'corporate' else '0px'} !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        border-bottom: 2px solid {t['border']} !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: {t['text_muted']} !important;
        font-family: {t['font_body']} !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: {t['accent_primary']} !important;
        border-bottom: 2px solid {t['accent_primary']} !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {t['bg_card']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
    }}

    /* DataFrame */
    .stDataFrame {{
        background-color: {t['bg_card']} !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {t['bg_secondary']};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {t['border']};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {t['accent_primary']};
    }}

    /* Positive/Negative colors */
    .positive {{ color: {t['positive']} !important; }}
    .negative {{ color: {t['negative']} !important; }}

    /* Corporate-specific refinements - Bloomberg/JP Morgan style */
    {f'''
    /* === CORPORATE BLOOMBERG STYLE === */

    /* Override everything with monospace terminal feel */
    .stApp {{
        font-family: {t['font_body']} !important;
        letter-spacing: 0.02em !important;
    }}

    /* Main container */
    .main .block-container {{
        padding: 1rem 2rem !important;
        max-width: 100% !important;
    }}

    /* Headers - clean, no decoration */
    h1 {{
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        border-bottom: 1px solid {t['border']} !important;
        padding-bottom: 0.5rem !important;
    }}

    h2, h3 {{
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: {t['accent_primary']} !important;
    }}

    /* Metrics - Bloomberg terminal style */
    [data-testid="stMetric"] {{
        background: {t['bg_card']} !important;
        border: 1px solid {t['border']} !important;
        border-left: 3px solid {t['accent_primary']} !important;
        border-radius: 0 !important;
        padding: 0.75rem 1rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-family: {t['font_body']} !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: {t['text_primary']} !important;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: {t['text_muted']} !important;
    }}

    [data-testid="stMetricDelta"] > div {{
        font-family: {t['font_body']} !important;
        font-size: 0.8rem !important;
    }}

    /* Sidebar - clean professional */
    [data-testid="stSidebar"] {{
        background: {t['bg_secondary']} !important;
        border-right: 1px solid {t['border']} !important;
    }}

    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label {{
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: {t['text_muted']} !important;
    }}

    /* Inputs - terminal style */
    .stTextInput input, .stNumberInput input {{
        background: {t['bg_primary']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 0 !important;
        font-family: {t['font_body']} !important;
        font-size: 0.9rem !important;
        color: {t['accent_secondary']} !important;
    }}

    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: {t['accent_primary']} !important;
        box-shadow: none !important;
    }}

    /* Select boxes */
    .stSelectbox > div > div {{
        background: {t['bg_primary']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 0 !important;
    }}

    /* Buttons - minimal */
    .stButton > button {{
        background: transparent !important;
        border: 1px solid {t['accent_primary']} !important;
        border-radius: 0 !important;
        color: {t['accent_primary']} !important;
        font-family: {t['font_body']} !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.15s ease !important;
    }}

    .stButton > button:hover {{
        background: {t['accent_primary']} !important;
        color: {t['bg_primary']} !important;
    }}

    /* Tabs - Bloomberg style */
    .stTabs [data-baseweb="tab-list"] {{
        background: {t['bg_secondary']} !important;
        border-bottom: none !important;
        gap: 0 !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border: 1px solid {t['border']} !important;
        border-bottom: none !important;
        border-radius: 0 !important;
        color: {t['text_muted']} !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 0.75rem 1.5rem !important;
        margin-right: -1px !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {t['bg_card']} !important;
        border-top: 2px solid {t['accent_primary']} !important;
        color: {t['text_primary']} !important;
    }}

    /* Tables */
    .stDataFrame {{
        border: 1px solid {t['border']} !important;
    }}

    .stDataFrame th {{
        background: {t['bg_secondary']} !important;
        color: {t['accent_primary']} !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    .stDataFrame td {{
        font-family: {t['font_body']} !important;
        font-size: 0.85rem !important;
        border-color: {t['border']} !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: {t['bg_secondary']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 0 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
    }}

    /* Checkbox */
    .stCheckbox label span {{
        font-size: 0.8rem !important;
    }}

    /* Slider */
    .stSlider > div > div > div {{
        background: {t['accent_primary']} !important;
    }}

    /* Spinner */
    .stSpinner > div {{
        border-color: {t['accent_primary']} transparent transparent transparent !important;
    }}

    /* Alerts/Info boxes */
    .stAlert {{
        background: {t['bg_card']} !important;
        border: 1px solid {t['border']} !important;
        border-left: 3px solid {t['accent_secondary']} !important;
        border-radius: 0 !important;
    }}

    /* Hide streamlit branding */
    #MainMenu, footer, header {{
        visibility: hidden !important;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 6px !important;
        height: 6px !important;
    }}

    ::-webkit-scrollbar-track {{
        background: {t['bg_primary']} !important;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {t['border']} !important;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {t['accent_primary']} !important;
    }}

    ''' if t['style'] == 'corporate' else ''}

    </style>
    """


def get_theme_title(main_text: str, subtitle_text: str = None):
    """Generate a themed title HTML."""
    t = get_theme()

    if t['style'] == 'corporate':
        # Elegant, understated corporate title
        return f"""<div style="text-align:left;padding:1rem 0;border-bottom:1px solid {t['border']};margin-bottom:1rem;">
            <h1 style="font-family:{t['font_title']};font-size:1.75rem;font-weight:500;color:{t['text_primary']};margin:0;letter-spacing:0.02em;">{main_text}</h1>
            {f'<span style="font-family:{t["font_body"]};font-size:0.8rem;color:{t["text_muted"]};letter-spacing:0.05em;">{subtitle_text}</span>' if subtitle_text else ''}
        </div>"""
    elif t['style'] == 'chaotic':
        # Original Raygun chaotic style
        return f"""<div style="text-align:center;padding:0.8rem 0;position:relative;">
            <div style="position:absolute;top:0;left:5%;width:90%;height:3px;background:linear-gradient(90deg,transparent,{t['accent_primary']},{t['accent_secondary']},{t['accent_primary']},transparent);"></div>
            <h1 style="font-family:{t['font_title']};font-size:clamp(2rem,8vw,4rem);letter-spacing:0.05em;text-transform:uppercase;color:{t['text_primary']};text-shadow:3px 3px 0 {t['accent_primary']},-2px -2px 0 {t['accent_secondary']},0 0 30px {t['accent_primary']}70;margin:0;line-height:1;">{main_text}</h1>
            {f'<div style="font-family:{t["font_body"]};font-size:0.6rem;letter-spacing:0.2em;color:{t["accent_secondary"]};text-transform:uppercase;margin-top:5px;">/// {subtitle_text} ///</div>' if subtitle_text else ''}
        </div>"""
    else:
        # Clean dark/light theme title
        return f"""<div style="text-align:center;padding:1rem 0;margin-bottom:1rem;">
            <h1 style="font-family:{t['font_title']};font-size:2rem;font-weight:600;color:{t['text_primary']};margin:0;">{main_text}</h1>
            {f'<span style="font-family:{t["font_body"]};font-size:0.85rem;color:{t["text_muted"]};">{subtitle_text}</span>' if subtitle_text else ''}
        </div>"""


# === PLOTLY TEMPLATE (Legacy - for backwards compatibility) ===
RAYGUN_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        # Background
        paper_bgcolor=COLORS['bg_dark'],
        plot_bgcolor=COLORS['bg_dark'],

        # Fonts
        font=dict(
            family='Space Mono, Consolas, monospace',
            color=COLORS['text_light'],
            size=11
        ),

        # Title
        title=dict(
            font=dict(
                family='Bebas Neue, Impact, sans-serif',
                size=28,
                color=COLORS['neon_pink']
            ),
            x=0.02,
            xanchor='left',
            y=0.98,
            yanchor='top'
        ),

        # X Axis
        xaxis=dict(
            gridcolor=COLORS['grid'],
            gridwidth=1,
            zerolinecolor=COLORS['neon_pink'],
            zerolinewidth=2,
            linecolor=COLORS['neon_cyan'],
            linewidth=2,
            tickfont=dict(
                family='Space Mono, monospace',
                size=9,
                color=COLORS['text_muted']
            ),
            title=dict(
                text='',
                font=dict(
                    family='Space Mono, monospace',
                    size=12,
                    color=COLORS['neon_cyan']
                )
            )
        ),

        # Y Axis
        yaxis=dict(
            gridcolor=COLORS['grid'],
            gridwidth=1,
            zerolinecolor=COLORS['neon_cyan'],
            zerolinewidth=2,
            linecolor=COLORS['neon_pink'],
            linewidth=2,
            tickfont=dict(
                family='Space Mono, monospace',
                size=9,
                color=COLORS['text_muted']
            ),
            title=dict(
                text='',
                font=dict(
                    family='Space Mono, monospace',
                    size=12,
                    color=COLORS['neon_pink']
                )
            )
        ),

        # Legend
        legend=dict(
            bgcolor='rgba(13, 13, 13, 0.9)',
            bordercolor=COLORS['neon_pink'],
            borderwidth=2,
            font=dict(
                family='Space Mono, monospace',
                size=10,
                color=COLORS['text_light']
            ),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),

        # Colorway for automatic coloring
        colorway=[
            COLORS['neon_pink'],
            COLORS['neon_cyan'],
            COLORS['neon_green'],
            COLORS['electric_yellow'],
            COLORS['hot_pink'],
            COLORS['grunge_orange'],
            COLORS['purple_haze'],
        ],

        # Hover
        hoverlabel=dict(
            bgcolor=COLORS['bg_card'],
            bordercolor=COLORS['neon_pink'],
            font=dict(
                family='Space Mono, monospace',
                size=12,
                color=COLORS['text_light']
            )
        ),

        # Annotations default
        annotationdefaults=dict(
            font=dict(
                family='Space Mono, monospace',
                size=11,
                color=COLORS['text_light']
            ),
            bgcolor=COLORS['bg_card'],
            bordercolor=COLORS['neon_cyan'],
            borderwidth=1
        )
    )
)

# Register the template
pio.templates['raygun'] = RAYGUN_TEMPLATE


def get_candlestick_colors():
    """Return candlestick color configuration."""
    return {
        'increasing_line_color': COLORS['candle_up'],
        'decreasing_line_color': COLORS['candle_down'],
        'increasing_fillcolor': COLORS['candle_up'],
        'decreasing_fillcolor': COLORS['candle_down'],
    }


def get_volume_colors(df):
    """Generate volume bar colors based on price movement."""
    return [
        COLORS['volume_down'] if df['close'].iloc[i] < df['open'].iloc[i]
        else COLORS['volume_up']
        for i in range(len(df))
    ]


def style_figure(fig, title=None):
    """Apply Raygun styling to a Plotly figure."""
    fig.update_layout(
        template='raygun',
        xaxis_rangeslider_visible=False,
        dragmode='zoom',
        hovermode='x unified',
    )

    if title:
        fig.update_layout(
            title=dict(
                text=f"<b>{title.upper()}</b>",
                font=dict(
                    family='Bebas Neue, Impact, sans-serif',
                    size=28,
                    color=COLORS['neon_pink']
                )
            )
        )

    # Style all xaxes and yaxes
    fig.update_xaxes(
        showgrid=True,
        gridcolor=COLORS['grid'],
        zeroline=True,
        zerolinecolor=COLORS['neon_pink'],
        showline=True,
        linecolor=COLORS['neon_cyan'],
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLORS['grid'],
        zeroline=True,
        zerolinecolor=COLORS['neon_cyan'],
        showline=True,
        linecolor=COLORS['neon_pink'],
    )

    return fig


def create_hline_style(y, color='neon_pink', dash='dash', annotation=None):
    """Create styled horizontal line parameters."""
    line_color = COLORS.get(color, color)
    result = dict(
        y=y,
        line_dash=dash,
        line_color=line_color,
        line_width=1,
        opacity=0.8
    )
    if annotation:
        result['annotation_text'] = annotation
        result['annotation_position'] = 'right'
        result['annotation_font'] = dict(
            family='Space Mono, monospace',
            size=10,
            color=line_color
        )
    return result


# === STREAMLIT CSS INJECTION ===
def get_streamlit_css():
    """Return CSS string for Streamlit injection."""
    try:
        import os
        # Try multiple paths
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'raygun_styles.css'),
            os.path.join(os.getcwd(), 'raygun_styles.css'),
            'raygun_styles.css',
            r'C:\Users\sango\Waza\OpenBB\raygun_styles.css'
        ]
        for css_path in possible_paths:
            if os.path.exists(css_path):
                with open(css_path, 'r', encoding='utf-8') as f:
                    return f.read()
        return ""
    except Exception as e:
        print(f"Error loading CSS: {e}")
        return ""


def get_corporate_css():
    """Return corporate CSS string for Streamlit injection."""
    try:
        import os
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'corporate_styles.css'),
            os.path.join(os.getcwd(), 'corporate_styles.css'),
            'corporate_styles.css',
        ]
        for css_path in possible_paths:
            if os.path.exists(css_path):
                with open(css_path, 'r', encoding='utf-8') as f:
                    return f.read()
        return ""
    except Exception as e:
        print(f"Error loading corporate CSS: {e}")
        return ""


def inject_corporate_css():
    """Inject Corporate CSS into Streamlit app."""
    import streamlit as st

    # First, inject the Material Symbols font directly
    material_font = """
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
    <style>
    /* Critical: Preserve Material Symbols for Streamlit icons */
    .material-symbols-rounded,
    span.material-symbols-rounded,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="baseButton-headerNoPadding"] span,
    button[kind="headerNoPadding"] span,
    .stPopover button span,
    [data-testid="stPopover"] button span {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 24px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
    }
    </style>
    """
    st.markdown(material_font, unsafe_allow_html=True)

    css = get_corporate_css()
    if css:
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # JavaScript to clean up inline neon styles
    corporate_js = """
    <script>
    (function() {
        const colorMap = {
            '#FF00FF': '#ff6600',
            '#ff00ff': '#ff6600',
            '#00FFFF': '#4a90d9',
            '#00ffff': '#4a90d9',
            '#39FF14': '#26a69a',
            '#39ff14': '#26a69a',
            '#FF3366': '#ef5350',
            '#ff3366': '#ef5350',
            '#FFE600': '#f7931a',
            '#ffe600': '#f7931a',
            'rgb(255, 0, 255)': '#ff6600',
            'rgb(0, 255, 255)': '#4a90d9',
            'rgb(57, 255, 20)': '#26a69a',
            'rgb(255, 51, 102)': '#ef5350'
        };

        function cleanCorporateStyles() {
            // Replace neon colors in inline styles
            document.querySelectorAll('[style]').forEach(el => {
                // Skip Material Icons elements
                if (el.classList.contains('material-symbols-rounded') ||
                    el.classList.contains('material-icons') ||
                    el.closest('.material-symbols-rounded')) {
                    return;
                }

                let style = el.getAttribute('style');
                if (!style) return;

                let modified = false;
                for (const [neon, corp] of Object.entries(colorMap)) {
                    if (style.includes(neon)) {
                        style = style.split(neon).join(corp);
                        modified = true;
                    }
                }

                // Remove text-shadow
                if (style.includes('text-shadow')) {
                    style = style.replace(/text-shadow:[^;]+;?/gi, 'text-shadow:none;');
                    modified = true;
                }

                // Remove transforms (skew, rotate)
                if (style.includes('skew') || style.includes('rotate')) {
                    style = style.replace(/transform:[^;]+;?/gi, 'transform:none;');
                    modified = true;
                }

                // Replace Bebas Neue font (but not Material Icons)
                if (style.includes('Bebas Neue') && !style.includes('Material')) {
                    style = style.replace(/font-family:[^;]+Bebas Neue[^;]*;?/gi,
                        "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;");
                    modified = true;
                }

                // Replace gradient backgrounds with solid
                if (style.includes('linear-gradient') &&
                    (style.includes('FF00FF') || style.includes('00FFFF') || style.includes('39FF14'))) {
                    style = style.replace(/background:[^;]*linear-gradient[^;]+;?/gi, 'background:#111111;');
                    modified = true;
                }

                if (modified) {
                    el.setAttribute('style', style);
                }
            });
        }

        // Run immediately and observe for changes
        cleanCorporateStyles();
        setTimeout(cleanCorporateStyles, 100);
        setTimeout(cleanCorporateStyles, 500);
        setTimeout(cleanCorporateStyles, 1500);

        const observer = new MutationObserver((mutations) => {
            let hasStyleChanges = mutations.some(m =>
                m.type === 'attributes' && m.attributeName === 'style' ||
                m.type === 'childList'
            );
            if (hasStyleChanges) {
                setTimeout(cleanCorporateStyles, 10);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style']
        });
    })();
    </script>
    """
    st.markdown(corporate_js, unsafe_allow_html=True)


def inject_theme_css():
    """Inject appropriate CSS based on current theme."""
    import streamlit as st
    theme = get_theme()

    if theme['style'] == 'corporate':
        inject_corporate_css()
    else:
        inject_raygun_css()

    # Always inject sidebar scroll fix
    sidebar_scroll_fix = """
    <script>
    (function() {
        function fixSidebarScroll() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                const firstDiv = sidebar.querySelector(':scope > div');
                if (firstDiv) {
                    firstDiv.style.overflowY = 'auto';
                    firstDiv.style.overflowX = 'hidden';
                    firstDiv.style.maxHeight = '100vh';
                }
            }
        }
        fixSidebarScroll();
        setTimeout(fixSidebarScroll, 500);
        setTimeout(fixSidebarScroll, 1500);
        const observer = new MutationObserver(fixSidebarScroll);
        const target = document.querySelector('[data-testid="stSidebar"]');
        if (target) {
            observer.observe(target, { childList: true, subtree: true });
        }
    })();
    </script>
    """
    st.markdown(sidebar_scroll_fix, unsafe_allow_html=True)


def inject_raygun_css():
    """Inject Raygun CSS into Streamlit app (only for non-corporate themes)."""
    import streamlit as st

    # Skip if corporate theme
    if get_theme()['style'] == 'corporate':
        return

    # Always inject Material Symbols font for icons
    material_font = """
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
    <style>
    /* Preserve Material Symbols for Streamlit icons - comprehensive selectors */
    .material-symbols-rounded,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] button span,
    [data-testid="stSidebarNavCollapseButton"] span,
    [data-testid="collapsedControl"] span,
    [data-testid="baseButton-headerNoPadding"] span,
    [data-testid="stPopover"] button span,
    button[kind="icon"] span,
    button[kind="headerNoPadding"] span,
    .stPopover span,
    /* Target floating expand button when sidebar is collapsed */
    [data-testid="stSidebar"][aria-expanded="false"] ~ div button span,
    div[data-testid="collapsedControl"] button span {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 24px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-feature-settings: 'liga' !important;
        font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        -webkit-font-smoothing: antialiased;
    }
    </style>
    """
    st.markdown(material_font, unsafe_allow_html=True)

    css = get_streamlit_css()
    if css:
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


# === THEME-AWARE DECORATIVE ELEMENTS ===

def get_header_decoration():
    """Return HTML for decorative header elements (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return ""  # No decoration in corporate mode
    return """<div style="position:relative;margin-bottom:1rem;padding:0.5rem;border-left:4px solid #FF00FF;background:linear-gradient(90deg,rgba(255,0,255,0.1) 0%,transparent 100%);"><span style="font-family:Space Mono,monospace;font-size:0.7rem;color:#888;letter-spacing:0.3em;text-transform:uppercase;">/// RAYGUN TERMINAL v1.0 ///</span></div>"""


def get_divider():
    """Return HTML for a stylized divider (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return """<div style="height:1px;margin:1.5rem 0;background:#2a2a2a;"></div>"""
    return """<div style="height: 2px; margin: 1.5rem 0; background: linear-gradient(90deg, transparent 0%, #FF00FF 20%, #00FFFF 50%, #FF00FF 80%, transparent 100%);"></div>"""


def get_glitch_title(text):
    """Return HTML for a glitch-effect title (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return f"""<h1 style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:1.25rem;font-weight:500;text-transform:uppercase;letter-spacing:0.08em;color:#f0f0f0;margin:0 0 0.5rem 0;padding:0 0 0.5rem 0;border-bottom:1px solid #2a2a2a;">{text}</h1>"""
    return f"""<h1 style="font-family:Bebas Neue,Impact,sans-serif;font-size:clamp(1.8rem,4vw,2.5rem);letter-spacing:0.08em;text-transform:uppercase;color:#E0E0E0;text-shadow:2px 2px 0 #FF00FF,-1px -1px 0 #00FFFF,3px 0 12px rgba(255,0,255,0.4);transform:rotate(-0.5deg);margin:0 0 0.25rem 0;padding:0;line-height:1.1;white-space:nowrap;border-bottom:none;">{text}</h1>"""


def get_sidebar_title(main_text, subtitle_text):
    """Return HTML for a properly structured sidebar title (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return f'<div style="padding:0.75rem 0;margin-bottom:1rem;border-bottom:1px solid #2a2a2a;"><h1 style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;font-size:1rem;font-weight:500;text-transform:uppercase;letter-spacing:0.1em;color:#f0f0f0;margin:0;">{main_text}</h1><span style="font-family:SF Mono,Consolas,monospace;font-size:0.65rem;letter-spacing:0.08em;color:#666;text-transform:uppercase;">{subtitle_text}</span></div>'
    return f"""<div style="display:flex;flex-direction:column;align-items:flex-start;padding:0.5rem 0;margin-bottom:1rem;position:relative;overflow:visible;"><div style="position:absolute;top:0;left:-10px;width:110%;height:3px;background:linear-gradient(90deg,#FF00FF,transparent);transform:rotate(-2deg);opacity:0.6;"></div><h1 class="sidebar-research-title" style="font-family:Bebas Neue,Impact,sans-serif;font-size:42px;letter-spacing:0.05em;text-transform:uppercase;color:#FF00FF;text-shadow:3px 3px 0 #00FFFF,-2px -2px 0 #39FF14,0 0 20px rgba(255,0,255,0.6);margin:0;padding:0;line-height:1;white-space:nowrap;overflow:visible;">{main_text}</h1><span style="font-family:Space Mono,monospace;font-size:0.85rem;letter-spacing:0.3em;color:#00FFFF;text-transform:uppercase;margin:6px 0 0 0;padding:0;line-height:1.2;">// {subtitle_text}</span><div style="width:100%;height:3px;margin-top:10px;background:linear-gradient(90deg,#FF00FF 0%,#00FFFF 50%,#39FF14 100%);box-shadow:0 0 10px #FF00FF;transform:skewX(-10deg);"></div></div>"""


def get_chaos_divider():
    """Return HTML for a chaotic Raygun divider (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return """<div style="height:1px;margin:1rem 0;background:#2a2a2a;"></div>"""
    return """<div style="position:relative;height:20px;margin:1rem 0;overflow:visible;"><div style="position:absolute;top:0;left:0;width:70%;height:2px;background:#FF00FF;transform:rotate(-1deg);"></div><div style="position:absolute;top:5px;left:15%;width:55%;height:1px;background:#00FFFF;transform:rotate(0.5deg);"></div><div style="position:absolute;top:10px;right:0;font-family:monospace;font-size:0.4rem;color:#39FF14;letter-spacing:0.2em;">[///]</div></div>"""


def get_section_header(text, number="01"):
    """Return HTML for a section header (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return f'<div style="margin:1.5rem 0 1rem 0;"><h2 style="font-family:SF Mono,Consolas,monospace;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.1em;color:#ff6600;border-left:3px solid #ff6600;padding-left:10px;margin:0;">{text}</h2></div>'
    return f"""<div style="position:relative;margin:1.5rem 0 1rem 0;"><span style="position:absolute;left:-12px;top:-8px;font-family:Bebas Neue,sans-serif;font-size:2.5rem;color:rgba(255,0,255,0.12);line-height:1;pointer-events:none;">{number}</span><h2 style="font-family:Space Mono,monospace;font-size:1.2rem;text-transform:uppercase;letter-spacing:0.12em;color:#00FFFF;border-left:5px solid #FF00FF;padding-left:12px;margin:0;transform:skewX(-1deg);">{text}</h2><div style="width:35%;height:2px;background:linear-gradient(90deg,#FF00FF,transparent);margin-top:4px;margin-left:17px;"></div></div>"""


def get_centered_title(main_text, subtitle_text):
    """Return HTML for a centered main title (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        # Corporate: clean left-aligned institutional title
        return f'<div style="text-align:left;padding:1rem 0;border-bottom:1px solid #2a2a2a;margin-bottom:1rem;"><h1 style="font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,sans-serif;font-size:1.5rem;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;color:#f0f0f0;margin:0;">{main_text}</h1><span style="font-family:SF Mono,Monaco,Consolas,monospace;font-size:0.7rem;letter-spacing:0.1em;color:#666;text-transform:uppercase;">{subtitle_text}</span></div>'
    # Raygun style - large neon title
    return f"""
    <style>
        .raygun-hero-container {{
            text-align: center;
            padding: 1.5rem 0 1rem 0;
            margin-bottom: 0.5rem;
            position: relative;
            width: 100%;
        }}
        .raygun-hero-container .gradient-line {{
            position: absolute;
            top: 0;
            left: 5%;
            width: 90%;
            height: 4px;
            background: linear-gradient(90deg, transparent, #FF00FF, #00FFFF, #FF00FF, transparent);
        }}
        .raygun-hero-container h1.raygun-main-title {{
            font-family: 'Bebas Neue', Impact, sans-serif !important;
            font-size: clamp(3rem, 10vw, 6rem) !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            color: #E0E0E0 !important;
            text-shadow: 4px 4px 0 #FF00FF, -3px -3px 0 #00FFFF, 0 0 40px rgba(255,0,255,0.7), 0 0 60px rgba(0,255,255,0.3) !important;
            margin: 0 !important;
            padding: 0.5rem 0 !important;
            line-height: 1.1 !important;
            display: block !important;
            width: 100% !important;
        }}
        .raygun-hero-container .raygun-subtitle {{
            font-family: 'Space Mono', monospace;
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            color: #00FFFF;
            text-transform: uppercase;
            margin-top: 8px;
            text-shadow: 0 0 10px rgba(0,255,255,0.6);
        }}
        .raygun-hero-container .bottom-gradient {{
            width: 60%;
            height: 3px;
            margin: 10px auto 0 auto;
            background: linear-gradient(90deg, transparent, #FF00FF 15%, #00FFFF 50%, #39FF14 85%, transparent);
            box-shadow: 0 0 15px rgba(255,0,255,0.5);
        }}
    </style>
    <div class="raygun-hero-container">
        <div class="gradient-line"></div>
        <h1 class="raygun-main-title">{main_text}</h1>
        <div class="raygun-subtitle">/// {subtitle_text} ///</div>
        <div class="bottom-gradient"></div>
    </div>
    """


def get_sidebar_section(title):
    """Return HTML for a sidebar section header (theme-aware)."""
    t = get_theme()
    if t['style'] == 'corporate':
        return f'<div style="font-family:SF Mono,Consolas,monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#666;border-left:2px solid #ff6600;padding-left:8px;margin:1.25rem 0 0.5rem 0;">{title}</div>'
    return f"""<div style="font-family:Bebas Neue,sans-serif;font-size:0.9rem;letter-spacing:0.08em;text-transform:uppercase;color:#66E0E0;border-left:3px solid #FF00FF;padding-left:10px;margin:1.5rem 0 0.75rem 0;padding-top:0.5rem;padding-bottom:0.25rem;text-shadow:0 0 6px rgba(102,224,224,0.4);border-top:1px solid rgba(255,0,255,0.2);">{title}</div>"""


def generate_ticker_html(stocks_data):
    """Generate HTML for the scrolling market ticker banner."""
    items_html = ""
    for stock in stocks_data:
        symbol = stock.get('symbol', '')
        price = stock.get('price', 0)
        change = stock.get('change', 0)
        change_pct = stock.get('change_pct', 0)
        is_index = stock.get('is_index', False)
        is_commodity = stock.get('is_commodity', False)

        change_class = 'positive' if change >= 0 else 'negative'
        change_sign = '+' if change >= 0 else ''

        if is_index:
            symbol_class = 'ticker-index'
        elif is_commodity:
            symbol_class = 'ticker-commodity'
        else:
            symbol_class = 'ticker-symbol'

        items_html += f'<div class="ticker-item"><span class="{symbol_class}">{symbol}</span><span class="ticker-price">${price:,.2f}</span><span class="ticker-change {change_class}">{change_sign}{change_pct:.2f}%</span></div>'

    # Duplicate for seamless loop
    full_items = items_html + items_html

    return f'<div class="ticker-wrap"><div class="ticker">{full_items}</div></div>'


def get_global_header(main_text, subtitle_text):
    """Return HTML for a fixed header spanning entire width."""
    return f"""<div class="raygun-global-header">
        <h1 class="raygun-header-title">{main_text}</h1>
        <span class="raygun-header-subtitle">/// {subtitle_text} ///</span>
    </div>"""


def get_global_footer(text):
    """Return HTML for a fixed footer spanning entire width."""
    return f"""<div class="raygun-global-footer">
        <span>{text}</span>
    </div>"""


def get_metric_card_header(text):
    """Return HTML for a metric card header."""
    t = get_theme()
    if get_theme_name() == "Corporate":
        return f'<div style="color:{t["accent_primary"]};font-weight:bold;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;padding-bottom:5px;border-bottom:1px solid {t["border"]};">{text}</div>'
    return f'<div style="color:{t["accent_primary"]};font-weight:bold;font-size:0.9rem;margin-bottom:10px;text-shadow:0 0 10px {t["accent_primary"]}40;">{text}</div>'


def get_subsection_header(text):
    """Return HTML for a subsection header."""
    t = get_theme()
    if get_theme_name() == "Corporate":
        return f'<div style="color:{t["accent_secondary"]};font-weight:bold;font-size:0.9rem;text-transform:uppercase;letter-spacing:0.05em;margin:15px 0 10px 0;padding-bottom:5px;border-bottom:1px solid {t["border"]};">{text}</div>'
    return f'<div style="color:{t["accent_secondary"]};font-weight:bold;font-size:1rem;margin:15px 0 10px 0;text-shadow:0 0 10px {t["accent_secondary"]}40;">{text}</div>'
