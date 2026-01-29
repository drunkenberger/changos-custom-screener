"""
Fund Screener Module
Buscador de Fondos y ETFs con filtros avanzados
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import yfinance as yf
from datetime import datetime, timedelta

# === UNIVERSO DE FONDOS Y ETFs ===
FUND_UNIVERSE = {
    "US Equity - Large Cap": [
        {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "issuer": "State Street"},
        {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "issuer": "Vanguard"},
        {"symbol": "IVV", "name": "iShares Core S&P 500", "issuer": "BlackRock"},
        {"symbol": "VTI", "name": "Vanguard Total Stock Market", "issuer": "Vanguard"},
        {"symbol": "QQQ", "name": "Invesco QQQ Trust", "issuer": "Invesco"},
        {"symbol": "VUG", "name": "Vanguard Growth ETF", "issuer": "Vanguard"},
        {"symbol": "VTV", "name": "Vanguard Value ETF", "issuer": "Vanguard"},
        {"symbol": "MGK", "name": "Vanguard Mega Cap Growth", "issuer": "Vanguard"},
        {"symbol": "SCHX", "name": "Schwab U.S. Large-Cap", "issuer": "Schwab"},
    ],
    "US Equity - Mid/Small Cap": [
        {"symbol": "IJH", "name": "iShares Core S&P Mid-Cap", "issuer": "BlackRock"},
        {"symbol": "IJR", "name": "iShares Core S&P Small-Cap", "issuer": "BlackRock"},
        {"symbol": "VB", "name": "Vanguard Small-Cap ETF", "issuer": "Vanguard"},
        {"symbol": "VO", "name": "Vanguard Mid-Cap ETF", "issuer": "Vanguard"},
        {"symbol": "IWM", "name": "iShares Russell 2000", "issuer": "BlackRock"},
        {"symbol": "VBK", "name": "Vanguard Small-Cap Growth", "issuer": "Vanguard"},
        {"symbol": "VBR", "name": "Vanguard Small-Cap Value", "issuer": "Vanguard"},
    ],
    "International Equity": [
        {"symbol": "VEA", "name": "Vanguard FTSE Developed", "issuer": "Vanguard"},
        {"symbol": "VWO", "name": "Vanguard FTSE Emerging", "issuer": "Vanguard"},
        {"symbol": "EFA", "name": "iShares MSCI EAFE", "issuer": "BlackRock"},
        {"symbol": "EEM", "name": "iShares MSCI Emerging", "issuer": "BlackRock"},
        {"symbol": "IEFA", "name": "iShares Core MSCI EAFE", "issuer": "BlackRock"},
        {"symbol": "VXUS", "name": "Vanguard Total International", "issuer": "Vanguard"},
        {"symbol": "VGK", "name": "Vanguard FTSE Europe", "issuer": "Vanguard"},
        {"symbol": "VPL", "name": "Vanguard FTSE Pacific", "issuer": "Vanguard"},
    ],
    "Fixed Income - Government": [
        {"symbol": "BND", "name": "Vanguard Total Bond Market", "issuer": "Vanguard"},
        {"symbol": "AGG", "name": "iShares Core US Aggregate", "issuer": "BlackRock"},
        {"symbol": "TLT", "name": "iShares 20+ Year Treasury", "issuer": "BlackRock"},
        {"symbol": "IEF", "name": "iShares 7-10 Year Treasury", "issuer": "BlackRock"},
        {"symbol": "SHY", "name": "iShares 1-3 Year Treasury", "issuer": "BlackRock"},
        {"symbol": "GOVT", "name": "iShares US Treasury Bond", "issuer": "BlackRock"},
        {"symbol": "VGSH", "name": "Vanguard Short-Term Treasury", "issuer": "Vanguard"},
        {"symbol": "VGIT", "name": "Vanguard Intermediate Treasury", "issuer": "Vanguard"},
    ],
    "Fixed Income - Corporate": [
        {"symbol": "LQD", "name": "iShares Investment Grade Corp", "issuer": "BlackRock"},
        {"symbol": "HYG", "name": "iShares High Yield Corp", "issuer": "BlackRock"},
        {"symbol": "VCIT", "name": "Vanguard Intermediate Corp", "issuer": "Vanguard"},
        {"symbol": "VCSH", "name": "Vanguard Short-Term Corp", "issuer": "Vanguard"},
        {"symbol": "JNK", "name": "SPDR Bloomberg High Yield", "issuer": "State Street"},
        {"symbol": "USIG", "name": "iShares Broad USD Inv Grade", "issuer": "BlackRock"},
    ],
    "Sector - Technology": [
        {"symbol": "XLK", "name": "Technology Select Sector", "issuer": "State Street"},
        {"symbol": "VGT", "name": "Vanguard Information Tech", "issuer": "Vanguard"},
        {"symbol": "SMH", "name": "VanEck Semiconductor", "issuer": "VanEck"},
        {"symbol": "ARKK", "name": "ARK Innovation ETF", "issuer": "ARK Invest"},
        {"symbol": "IGV", "name": "iShares Expanded Tech-Software", "issuer": "BlackRock"},
        {"symbol": "SOXX", "name": "iShares Semiconductor", "issuer": "BlackRock"},
    ],
    "Sector - Healthcare": [
        {"symbol": "XLV", "name": "Health Care Select Sector", "issuer": "State Street"},
        {"symbol": "VHT", "name": "Vanguard Health Care", "issuer": "Vanguard"},
        {"symbol": "IBB", "name": "iShares Biotechnology", "issuer": "BlackRock"},
        {"symbol": "XBI", "name": "SPDR S&P Biotech", "issuer": "State Street"},
        {"symbol": "IHI", "name": "iShares US Medical Devices", "issuer": "BlackRock"},
    ],
    "Sector - Financials": [
        {"symbol": "XLF", "name": "Financial Select Sector", "issuer": "State Street"},
        {"symbol": "VFH", "name": "Vanguard Financials", "issuer": "Vanguard"},
        {"symbol": "KBE", "name": "SPDR S&P Bank ETF", "issuer": "State Street"},
        {"symbol": "KRE", "name": "SPDR S&P Regional Banking", "issuer": "State Street"},
    ],
    "Sector - Energy": [
        {"symbol": "XLE", "name": "Energy Select Sector", "issuer": "State Street"},
        {"symbol": "VDE", "name": "Vanguard Energy", "issuer": "Vanguard"},
        {"symbol": "OIH", "name": "VanEck Oil Services", "issuer": "VanEck"},
        {"symbol": "XOP", "name": "SPDR S&P Oil & Gas Exploration", "issuer": "State Street"},
    ],
    "Sector - Real Estate": [
        {"symbol": "VNQ", "name": "Vanguard Real Estate", "issuer": "Vanguard"},
        {"symbol": "XLRE", "name": "Real Estate Select Sector", "issuer": "State Street"},
        {"symbol": "IYR", "name": "iShares US Real Estate", "issuer": "BlackRock"},
        {"symbol": "SCHH", "name": "Schwab US REIT", "issuer": "Schwab"},
    ],
    "Commodities": [
        {"symbol": "GLD", "name": "SPDR Gold Shares", "issuer": "State Street"},
        {"symbol": "IAU", "name": "iShares Gold Trust", "issuer": "BlackRock"},
        {"symbol": "SLV", "name": "iShares Silver Trust", "issuer": "BlackRock"},
        {"symbol": "USO", "name": "United States Oil Fund", "issuer": "USCF"},
        {"symbol": "DBC", "name": "Invesco DB Commodity", "issuer": "Invesco"},
        {"symbol": "PDBC", "name": "Invesco Optimum Yield Diversified", "issuer": "Invesco"},
    ],
    "Dividend & Income": [
        {"symbol": "VYM", "name": "Vanguard High Dividend Yield", "issuer": "Vanguard"},
        {"symbol": "SCHD", "name": "Schwab US Dividend Equity", "issuer": "Schwab"},
        {"symbol": "DVY", "name": "iShares Select Dividend", "issuer": "BlackRock"},
        {"symbol": "HDV", "name": "iShares Core High Dividend", "issuer": "BlackRock"},
        {"symbol": "VIG", "name": "Vanguard Dividend Appreciation", "issuer": "Vanguard"},
        {"symbol": "DGRO", "name": "iShares Core Dividend Growth", "issuer": "BlackRock"},
    ],
    "ESG & Sustainable": [
        {"symbol": "ESGU", "name": "iShares ESG Aware MSCI USA", "issuer": "BlackRock"},
        {"symbol": "ESGV", "name": "Vanguard ESG US Stock", "issuer": "Vanguard"},
        {"symbol": "SUSA", "name": "iShares MSCI USA ESG Select", "issuer": "BlackRock"},
        {"symbol": "ICLN", "name": "iShares Global Clean Energy", "issuer": "BlackRock"},
        {"symbol": "QCLN", "name": "First Trust NASDAQ Clean Edge", "issuer": "First Trust"},
    ],
    "Multi-Asset & Balanced": [
        {"symbol": "AOR", "name": "iShares Core Growth Allocation", "issuer": "BlackRock"},
        {"symbol": "AOM", "name": "iShares Core Moderate Allocation", "issuer": "BlackRock"},
        {"symbol": "AOK", "name": "iShares Core Conservative Allocation", "issuer": "BlackRock"},
        {"symbol": "AOA", "name": "iShares Core Aggressive Allocation", "issuer": "BlackRock"},
    ],
}


def get_all_fund_symbols() -> List[str]:
    """Retorna lista de todos los símbolos del universo."""
    symbols = []
    for category in FUND_UNIVERSE.values():
        for fund in category:
            symbols.append(fund["symbol"])
    return symbols


def get_categories() -> List[str]:
    """Retorna lista de categorías disponibles."""
    return list(FUND_UNIVERSE.keys())


def get_funds_by_category(category: str) -> List[Dict]:
    """Retorna fondos de una categoría específica."""
    return FUND_UNIVERSE.get(category, [])


def fetch_fund_data(symbol: str) -> Dict:
    """
    Obtiene datos completos de un fondo/ETF.

    Returns:
        Dict con métricas del fondo
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Obtener historial para cálculos
        hist = ticker.history(period="1y")

        # Calcular métricas
        if not hist.empty:
            returns = hist['Close'].pct_change().dropna()
            annual_return = (1 + returns.mean()) ** 252 - 1
            volatility = returns.std() * np.sqrt(252)
            sharpe = annual_return / volatility if volatility > 0 else 0

            # Calcular drawdown máximo
            cumulative = (1 + returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
        else:
            annual_return = 0
            volatility = 0
            sharpe = 0
            max_drawdown = 0

        # Buscar info de categoría
        category = None
        issuer = None
        for cat_name, funds in FUND_UNIVERSE.items():
            for fund in funds:
                if fund["symbol"] == symbol:
                    category = cat_name
                    issuer = fund.get("issuer", "Unknown")
                    break
            if category:
                break

        return {
            "symbol": symbol,
            "name": info.get("longName", info.get("shortName", symbol)),
            "category": category or info.get("category", "Unknown"),
            "issuer": issuer or "Unknown",
            "price": info.get("regularMarketPrice", info.get("navPrice", 0)),
            "aum": info.get("totalAssets", 0),
            "expense_ratio": info.get("annualReportExpenseRatio", 0) or 0,
            "dividend_yield": info.get("yield", 0) or 0,
            "beta": info.get("beta3Year", info.get("beta", 1.0)) or 1.0,
            "annual_return": annual_return * 100,
            "volatility": volatility * 100,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_drawdown * 100,
            "52w_high": info.get("fiftyTwoWeekHigh", 0),
            "52w_low": info.get("fiftyTwoWeekLow", 0),
            "avg_volume": info.get("averageVolume", 0),
            "holdings_count": info.get("holdings", 0),
            "inception_date": info.get("fundInceptionDate", None),
            "description": info.get("longBusinessSummary", ""),
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return {"symbol": symbol, "error": str(e)}


def fetch_multiple_funds(symbols: List[str]) -> pd.DataFrame:
    """
    Obtiene datos de múltiples fondos.

    Returns:
        DataFrame con datos de todos los fondos
    """
    results = []
    for symbol in symbols:
        data = fetch_fund_data(symbol)
        if "error" not in data:
            results.append(data)

    return pd.DataFrame(results)


def filter_funds(
    df: pd.DataFrame,
    category: Optional[str] = None,
    min_aum: Optional[float] = None,
    max_expense_ratio: Optional[float] = None,
    min_sharpe: Optional[float] = None,
    min_dividend_yield: Optional[float] = None,
    max_volatility: Optional[float] = None,
    issuer: Optional[str] = None,
) -> pd.DataFrame:
    """
    Filtra fondos según criterios.

    Args:
        df: DataFrame con datos de fondos
        category: Filtrar por categoría
        min_aum: AUM mínimo en USD
        max_expense_ratio: Expense ratio máximo (decimal)
        min_sharpe: Sharpe ratio mínimo
        min_dividend_yield: Dividend yield mínimo (decimal)
        max_volatility: Volatilidad máxima (%)
        issuer: Filtrar por emisor

    Returns:
        DataFrame filtrado
    """
    filtered = df.copy()

    if category and category != "Todas":
        filtered = filtered[filtered["category"] == category]

    if min_aum:
        filtered = filtered[filtered["aum"] >= min_aum]

    if max_expense_ratio:
        filtered = filtered[filtered["expense_ratio"] <= max_expense_ratio]

    if min_sharpe:
        filtered = filtered[filtered["sharpe_ratio"] >= min_sharpe]

    if min_dividend_yield:
        filtered = filtered[filtered["dividend_yield"] >= min_dividend_yield]

    if max_volatility:
        filtered = filtered[filtered["volatility"] <= max_volatility]

    if issuer and issuer != "Todos":
        filtered = filtered[filtered["issuer"] == issuer]

    return filtered


def get_fund_comparison(symbols: List[str], period: str = "1y") -> pd.DataFrame:
    """
    Compara rendimiento de múltiples fondos.

    Returns:
        DataFrame con precios normalizados para comparación
    """
    try:
        data = yf.download(symbols, period=period, progress=False)['Close']

        if data.empty:
            return pd.DataFrame()

        # Normalizar a 100
        normalized = data / data.iloc[0] * 100

        return normalized
    except Exception as e:
        print(f"Error comparing funds: {e}")
        return pd.DataFrame()


def get_fund_metrics_summary(symbol: str) -> Dict:
    """
    Obtiene resumen de métricas clave para un fondo.
    """
    data = fetch_fund_data(symbol)

    if "error" in data:
        return data

    # Calcular rating simple basado en métricas
    score = 0
    if data["sharpe_ratio"] > 1:
        score += 2
    elif data["sharpe_ratio"] > 0.5:
        score += 1

    if data["expense_ratio"] < 0.001:  # < 0.1%
        score += 2
    elif data["expense_ratio"] < 0.005:  # < 0.5%
        score += 1

    if data["max_drawdown"] > -20:
        score += 1

    if data["annual_return"] > 10:
        score += 2
    elif data["annual_return"] > 5:
        score += 1

    # Rating de 1 a 5 estrellas
    rating = min(5, max(1, score))

    data["rating"] = rating
    data["rating_label"] = "★" * rating + "☆" * (5 - rating)

    return data


def format_aum(value: float) -> str:
    """Formatea AUM en formato legible."""
    if value >= 1e12:
        return f"${value/1e12:.1f}T"
    elif value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    else:
        return f"${value:,.0f}"


def get_ai_fund_analysis(
    fund_data: Dict,
    api_key: Optional[str] = None
) -> str:
    """
    Genera análisis de IA para un fondo.

    Args:
        fund_data: Diccionario con datos del fondo
        api_key: API key de Anthropic

    Returns:
        Análisis en texto generado por IA
    """
    if api_key is None:
        return get_fallback_fund_analysis(fund_data)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""Eres un analista financiero experto en ETFs y fondos de inversión.

Analiza el siguiente fondo y proporciona un análisis conciso:

**FONDO ANALIZADO:**
- Símbolo: {fund_data.get('symbol', 'N/A')}
- Nombre: {fund_data.get('name', 'N/A')}
- Categoría: {fund_data.get('category', 'N/A')}
- Emisor: {fund_data.get('issuer', 'N/A')}

**MÉTRICAS CLAVE:**
- AUM: {format_aum(fund_data.get('aum', 0))}
- Expense Ratio: {fund_data.get('expense_ratio', 0)*100:.2f}%
- Rendimiento Anual: {fund_data.get('annual_return', 0):.2f}%
- Volatilidad: {fund_data.get('volatility', 0):.2f}%
- Sharpe Ratio: {fund_data.get('sharpe_ratio', 0):.2f}
- Beta: {fund_data.get('beta', 1.0):.2f}
- Max Drawdown: {fund_data.get('max_drawdown', 0):.2f}%
- Dividend Yield: {fund_data.get('dividend_yield', 0)*100:.2f}%

Proporciona un análisis en español con:
1. **Evaluación General**: Resumen de 2-3 líneas sobre el fondo
2. **Puntos Fuertes**: 2-3 aspectos positivos
3. **Puntos de Atención**: 2-3 riesgos o consideraciones
4. **Perfil de Inversor Ideal**: Para quién es apropiado este fondo
5. **Veredicto**: Recomendación final concisa

Mantén la respuesta concisa y accionable (máximo 250 palabras)."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    except ImportError:
        return get_fallback_fund_analysis(fund_data)
    except Exception as e:
        print(f"Error en análisis de IA: {e}")
        return get_fallback_fund_analysis(fund_data)


def get_fallback_fund_analysis(fund_data: Dict) -> str:
    """Genera análisis básico sin IA."""

    symbol = fund_data.get('symbol', 'N/A')
    name = fund_data.get('name', 'N/A')
    category = fund_data.get('category', 'N/A')

    sharpe = fund_data.get('sharpe_ratio', 0)
    expense = fund_data.get('expense_ratio', 0) * 100
    annual_ret = fund_data.get('annual_return', 0)
    volatility = fund_data.get('volatility', 0)

    # Evaluaciones
    sharpe_eval = "excelente" if sharpe > 1 else "bueno" if sharpe > 0.5 else "moderado"
    expense_eval = "muy bajo" if expense < 0.1 else "bajo" if expense < 0.5 else "moderado"

    analysis = f"""**Análisis de {symbol} - {name}**

**Evaluación General:**
{name} es un ETF de la categoría {category} con un perfil de riesgo-retorno {sharpe_eval}.

**Métricas Destacadas:**
- Sharpe Ratio de {sharpe:.2f} ({sharpe_eval})
- Expense Ratio de {expense:.2f}% ({expense_eval})
- Rendimiento anual de {annual_ret:.2f}%
- Volatilidad de {volatility:.2f}%

**Consideraciones:**
- {'Buena relación riesgo-retorno' if sharpe > 0.5 else 'Considerar alternativas con mejor Sharpe'}
- {'Costos competitivos' if expense < 0.5 else 'Evaluar alternativas de menor costo'}

**Nota:** Este análisis es informativo. Consulta a un asesor financiero antes de invertir."""

    return analysis


# === QUICK SEARCH ===
def search_funds(query: str) -> List[Dict]:
    """
    Búsqueda rápida de fondos por nombre o símbolo.
    """
    query = query.upper()
    results = []

    for category, funds in FUND_UNIVERSE.items():
        for fund in funds:
            if query in fund["symbol"] or query in fund["name"].upper():
                results.append({
                    **fund,
                    "category": category
                })

    return results
