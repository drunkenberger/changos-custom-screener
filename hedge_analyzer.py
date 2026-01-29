"""
Hedge Analyzer Module
Analiza correlaciones y sugiere activos para hedge
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import yfinance as yf
from datetime import datetime, timedelta

# Universo de activos para análisis de correlación
HEDGE_UNIVERSE = {
    "Índices Inversos": [
        {"symbol": "SH", "name": "ProShares Short S&P500", "description": "ETF inverso del S&P 500"},
        {"symbol": "PSQ", "name": "ProShares Short QQQ", "description": "ETF inverso del Nasdaq"},
        {"symbol": "DOG", "name": "ProShares Short Dow30", "description": "ETF inverso del Dow Jones"},
        {"symbol": "RWM", "name": "ProShares Short Russell2000", "description": "ETF inverso del Russell 2000"},
    ],
    "Volatilidad": [
        {"symbol": "VXX", "name": "iPath VIX Short-Term", "description": "Exposición a volatilidad corto plazo"},
        {"symbol": "UVXY", "name": "ProShares Ultra VIX", "description": "2x volatilidad corto plazo"},
        {"symbol": "VIXY", "name": "ProShares VIX Short-Term", "description": "Futuros VIX corto plazo"},
    ],
    "Metales Preciosos": [
        {"symbol": "GLD", "name": "SPDR Gold Shares", "description": "Oro físico"},
        {"symbol": "SLV", "name": "iShares Silver Trust", "description": "Plata física"},
        {"symbol": "GDX", "name": "VanEck Gold Miners", "description": "Mineras de oro"},
        {"symbol": "IAU", "name": "iShares Gold Trust", "description": "Oro físico alternativo"},
    ],
    "Bonos/Renta Fija": [
        {"symbol": "TLT", "name": "iShares 20+ Year Treasury", "description": "Bonos del tesoro largo plazo"},
        {"symbol": "IEF", "name": "iShares 7-10 Year Treasury", "description": "Bonos del tesoro mediano plazo"},
        {"symbol": "BND", "name": "Vanguard Total Bond", "description": "Bonos diversificados"},
        {"symbol": "TIPS", "name": "iShares TIPS Bond", "description": "Bonos protegidos contra inflación"},
    ],
    "Commodities": [
        {"symbol": "USO", "name": "United States Oil Fund", "description": "Petróleo"},
        {"symbol": "UNG", "name": "United States Natural Gas", "description": "Gas natural"},
        {"symbol": "DBA", "name": "Invesco DB Agriculture", "description": "Agricultura diversificada"},
        {"symbol": "DBB", "name": "Invesco DB Base Metals", "description": "Metales base"},
    ],
    "Divisas": [
        {"symbol": "UUP", "name": "Invesco DB US Dollar", "description": "Dólar estadounidense"},
        {"symbol": "FXE", "name": "Invesco CurrencyShares Euro", "description": "Euro"},
        {"symbol": "FXY", "name": "Invesco CurrencyShares Yen", "description": "Yen japonés"},
        {"symbol": "FXF", "name": "Invesco CurrencyShares Franc", "description": "Franco suizo"},
    ],
    "Sectores Defensivos": [
        {"symbol": "XLU", "name": "Utilities Select Sector", "description": "Sector utilities"},
        {"symbol": "XLP", "name": "Consumer Staples Select", "description": "Consumo básico"},
        {"symbol": "XLV", "name": "Health Care Select", "description": "Sector salud"},
        {"symbol": "VNQ", "name": "Vanguard Real Estate", "description": "Bienes raíces"},
    ],
    "Mercados Internacionales": [
        {"symbol": "EFA", "name": "iShares MSCI EAFE", "description": "Mercados desarrollados ex-US"},
        {"symbol": "EEM", "name": "iShares MSCI Emerging", "description": "Mercados emergentes"},
        {"symbol": "VEA", "name": "Vanguard FTSE Developed", "description": "Mercados desarrollados"},
        {"symbol": "VWO", "name": "Vanguard FTSE Emerging", "description": "Mercados emergentes"},
    ],
}


def get_all_hedge_symbols() -> List[str]:
    """Retorna lista de todos los símbolos del universo de hedge."""
    symbols = []
    for category in HEDGE_UNIVERSE.values():
        for asset in category:
            symbols.append(asset["symbol"])
    return symbols


def calculate_correlations(
    ticker: str,
    period: str = "1y",
    hedge_symbols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calcula correlaciones entre el ticker y el universo de hedge.

    Args:
        ticker: Símbolo del activo principal
        period: Período de análisis (1y, 2y, 6mo)
        hedge_symbols: Lista opcional de símbolos, si no se da usa el universo completo

    Returns:
        DataFrame con correlaciones ordenadas de menor a mayor
    """
    if hedge_symbols is None:
        hedge_symbols = get_all_hedge_symbols()

    # Agregar el ticker principal a la lista
    all_symbols = [ticker] + hedge_symbols

    try:
        # Descargar datos históricos
        data = yf.download(all_symbols, period=period, progress=False)['Close']

        if data.empty:
            return pd.DataFrame()

        # Calcular retornos diarios
        returns = data.pct_change().dropna()

        if returns.empty or ticker not in returns.columns:
            return pd.DataFrame()

        # Calcular matriz de correlación
        corr_matrix = returns.corr()

        # Extraer correlaciones con el ticker principal
        if ticker in corr_matrix.columns:
            correlations = corr_matrix[ticker].drop(ticker)
        else:
            return pd.DataFrame()

        # Crear DataFrame con información adicional
        results = []
        for symbol, corr in correlations.items():
            if pd.notna(corr):
                # Buscar información del símbolo
                asset_info = None
                category_name = None
                for cat_name, assets in HEDGE_UNIVERSE.items():
                    for asset in assets:
                        if asset["symbol"] == symbol:
                            asset_info = asset
                            category_name = cat_name
                            break
                    if asset_info:
                        break

                results.append({
                    "symbol": symbol,
                    "name": asset_info["name"] if asset_info else symbol,
                    "description": asset_info["description"] if asset_info else "",
                    "category": category_name or "Otro",
                    "correlation": corr,
                    "hedge_score": calculate_hedge_score(corr)
                })

        df = pd.DataFrame(results)
        if not df.empty:
            df = df.sort_values("correlation", ascending=True)

        return df

    except Exception as e:
        print(f"Error calculando correlaciones: {e}")
        return pd.DataFrame()


def calculate_hedge_score(correlation: float) -> str:
    """
    Calcula un score de hedge basado en la correlación.
    Correlación negativa = mejor hedge
    """
    if correlation <= -0.5:
        return "EXCELENTE"
    elif correlation <= -0.2:
        return "MUY BUENO"
    elif correlation <= 0:
        return "BUENO"
    elif correlation <= 0.3:
        return "MODERADO"
    elif correlation <= 0.6:
        return "BAJO"
    else:
        return "NO RECOMENDADO"


def get_hedge_score_color(score: str) -> str:
    """Retorna color CSS para el score de hedge."""
    colors = {
        "EXCELENTE": "#39FF14",
        "MUY BUENO": "#00FFFF",
        "BUENO": "#7B68EE",
        "MODERADO": "#FFD700",
        "BAJO": "#FF8C00",
        "NO RECOMENDADO": "#FF3366"
    }
    return colors.get(score, "#888888")


def get_top_hedges(
    ticker: str,
    top_n: int = 10,
    period: str = "1y"
) -> List[Dict]:
    """
    Obtiene los mejores activos de hedge para un ticker.

    Args:
        ticker: Símbolo del activo principal
        top_n: Número de resultados a retornar
        period: Período de análisis

    Returns:
        Lista de diccionarios con los mejores hedges
    """
    df = calculate_correlations(ticker, period)

    if df.empty:
        return []

    # Filtrar solo correlaciones bajas o negativas
    df_hedges = df[df["correlation"] < 0.5]

    return df_hedges.head(top_n).to_dict("records")


def analyze_portfolio_hedge(
    ticker: str,
    hedge_symbol: str,
    allocation_pct: float = 20,
    period: str = "1y"
) -> Dict:
    """
    Analiza el impacto de agregar un hedge al portafolio.

    Args:
        ticker: Activo principal
        hedge_symbol: Activo de hedge
        allocation_pct: Porcentaje del portafolio para el hedge
        period: Período de análisis

    Returns:
        Diccionario con métricas del portafolio
    """
    try:
        data = yf.download([ticker, hedge_symbol], period=period, progress=False)['Close']

        if data.empty:
            return {}

        returns = data.pct_change().dropna()

        # Portafolio original (100% ticker)
        original_returns = returns[ticker]
        original_vol = original_returns.std() * np.sqrt(252)
        original_return = (1 + original_returns).prod() ** (252/len(original_returns)) - 1
        original_sharpe = original_return / original_vol if original_vol > 0 else 0

        # Portafolio con hedge
        hedge_weight = allocation_pct / 100
        ticker_weight = 1 - hedge_weight

        portfolio_returns = returns[ticker] * ticker_weight + returns[hedge_symbol] * hedge_weight
        portfolio_vol = portfolio_returns.std() * np.sqrt(252)
        portfolio_return = (1 + portfolio_returns).prod() ** (252/len(portfolio_returns)) - 1
        portfolio_sharpe = portfolio_return / portfolio_vol if portfolio_vol > 0 else 0

        # Calcular correlación
        correlation = returns[ticker].corr(returns[hedge_symbol])

        return {
            "original_volatility": original_vol * 100,
            "hedged_volatility": portfolio_vol * 100,
            "volatility_reduction": (original_vol - portfolio_vol) / original_vol * 100 if original_vol > 0 else 0,
            "original_return": original_return * 100,
            "hedged_return": portfolio_return * 100,
            "original_sharpe": original_sharpe,
            "hedged_sharpe": portfolio_sharpe,
            "correlation": correlation,
            "hedge_allocation": allocation_pct
        }

    except Exception as e:
        print(f"Error analizando hedge: {e}")
        return {}


# === AI AGENT FOR HEDGE RECOMMENDATIONS ===

def get_ai_hedge_analysis(
    ticker: str,
    correlations_df: pd.DataFrame,
    ticker_info: Dict,
    api_key: Optional[str] = None
) -> str:
    """
    Usa IA para generar análisis y recomendaciones de hedge personalizadas.

    Args:
        ticker: Símbolo del activo
        correlations_df: DataFrame con correlaciones calculadas
        ticker_info: Información del ticker (sector, industry, etc)
        api_key: API key de Anthropic

    Returns:
        Análisis en texto generado por IA
    """
    if api_key is None:
        return get_fallback_analysis(ticker, correlations_df, ticker_info)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        # Preparar contexto para el agente
        top_hedges = correlations_df.head(5).to_dict("records") if not correlations_df.empty else []
        worst_hedges = correlations_df.tail(3).to_dict("records") if not correlations_df.empty else []

        sector = ticker_info.get("sector", "Desconocido")
        industry = ticker_info.get("industry", "Desconocido")
        beta = ticker_info.get("beta", 1.0)

        prompt = f"""Eres un analista financiero experto en gestión de riesgos y construcción de portafolios.

Analiza el siguiente activo y proporciona recomendaciones de hedge personalizadas:

**ACTIVO ANALIZADO:**
- Ticker: {ticker}
- Sector: {sector}
- Industria: {industry}
- Beta: {beta}

**MEJORES OPCIONES DE HEDGE (menor correlación):**
{top_hedges}

**ACTIVOS A EVITAR COMO HEDGE (alta correlación):**
{worst_hedges}

Proporciona un análisis conciso en español con:
1. **Resumen de Riesgo**: Evaluación breve del perfil de riesgo del activo
2. **Top 3 Recomendaciones de Hedge**: Los mejores activos para proteger la posición, explicando por qué
3. **Estrategia Sugerida**: Porcentaje recomendado de asignación al hedge
4. **Advertencias**: Factores a considerar o riesgos del hedge

Mantén la respuesta concisa y accionable (máximo 300 palabras)."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    except ImportError:
        return get_fallback_analysis(ticker, correlations_df, ticker_info)
    except Exception as e:
        print(f"Error en análisis de IA: {e}")
        return get_fallback_analysis(ticker, correlations_df, ticker_info)


def get_fallback_analysis(
    ticker: str,
    correlations_df: pd.DataFrame,
    ticker_info: Dict
) -> str:
    """Genera análisis básico sin IA cuando no está disponible."""

    if correlations_df.empty:
        return "No se pudieron calcular correlaciones. Verifica que el ticker sea válido."

    sector = ticker_info.get("sector", "Desconocido")
    beta = ticker_info.get("beta", 1.0)

    top_hedges = correlations_df.head(3)

    analysis = f"""**Análisis de Hedge para {ticker}**

**Perfil de Riesgo:**
- Sector: {sector}
- Beta: {beta:.2f} {'(más volátil que el mercado)' if beta > 1 else '(menos volátil que el mercado)' if beta < 1 else '(igual al mercado)'}

**Top 3 Recomendaciones de Hedge:**
"""

    for i, row in top_hedges.iterrows():
        analysis += f"""
{row['symbol']} - {row['name']}
- Correlación: {row['correlation']:.2f}
- Score: {row['hedge_score']}
- {row['description']}
"""

    analysis += """
**Estrategia Sugerida:**
- Asignar 10-20% del portafolio a activos de hedge
- Diversificar entre diferentes categorías (metales, bonos, volatilidad)
- Rebalancear trimestralmente

**Nota:** Este análisis es informativo. Consulta a un asesor financiero antes de tomar decisiones de inversión."""

    return analysis
