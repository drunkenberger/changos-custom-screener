"""
Portfolio Generator Module
Generador de portafolios con IA y templates predefinidos
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import yfinance as yf
from datetime import datetime, timedelta

# === PERFILES DE RIESGO ===
RISK_PROFILES = {
    "Conservador": {
        "description": "Prioriza preservación de capital con bajo riesgo",
        "target_volatility": 8,
        "equity_range": (20, 40),
        "bond_range": (50, 70),
        "alternative_range": (0, 10),
        "max_single_position": 25,
    },
    "Moderado": {
        "description": "Balance entre crecimiento y estabilidad",
        "target_volatility": 12,
        "equity_range": (40, 60),
        "bond_range": (30, 50),
        "alternative_range": (5, 15),
        "max_single_position": 20,
    },
    "Agresivo": {
        "description": "Busca máximo crecimiento, tolera alta volatilidad",
        "target_volatility": 18,
        "equity_range": (70, 90),
        "bond_range": (5, 20),
        "alternative_range": (5, 15),
        "max_single_position": 25,
    },
    "Muy Agresivo": {
        "description": "100% enfocado en crecimiento, máxima tolerancia al riesgo",
        "target_volatility": 25,
        "equity_range": (85, 100),
        "bond_range": (0, 10),
        "alternative_range": (0, 15),
        "max_single_position": 30,
    },
}

# === HORIZONTES DE INVERSIÓN ===
INVESTMENT_HORIZONS = {
    "Corto Plazo (1-3 años)": {
        "years": 2,
        "focus": "Liquidez y preservación",
        "equity_adjustment": -15,
        "bond_adjustment": 15,
    },
    "Mediano Plazo (3-7 años)": {
        "years": 5,
        "focus": "Balance crecimiento/estabilidad",
        "equity_adjustment": 0,
        "bond_adjustment": 0,
    },
    "Largo Plazo (7-15 años)": {
        "years": 10,
        "focus": "Crecimiento con tiempo para recuperar",
        "equity_adjustment": 10,
        "bond_adjustment": -10,
    },
    "Muy Largo Plazo (15+ años)": {
        "years": 20,
        "focus": "Máximo crecimiento compuesto",
        "equity_adjustment": 15,
        "bond_adjustment": -15,
    },
}

# === TEMPLATES DE PORTAFOLIO ===
PORTFOLIO_TEMPLATES = {
    "Classic 60/40": {
        "description": "Portafolio tradicional balanceado",
        "risk_level": "Moderado",
        "allocations": [
            {"symbol": "VTI", "weight": 40, "category": "US Equity"},
            {"symbol": "VXUS", "weight": 20, "category": "International Equity"},
            {"symbol": "BND", "weight": 30, "category": "US Bonds"},
            {"symbol": "BNDX", "weight": 10, "category": "International Bonds"},
        ],
    },
    "Three Fund Portfolio": {
        "description": "Portafolio Boglehead de 3 fondos",
        "risk_level": "Moderado",
        "allocations": [
            {"symbol": "VTI", "weight": 50, "category": "US Total Market"},
            {"symbol": "VXUS", "weight": 30, "category": "International"},
            {"symbol": "BND", "weight": 20, "category": "Bonds"},
        ],
    },
    "All Weather": {
        "description": "Portafolio Ray Dalio para cualquier escenario",
        "risk_level": "Conservador",
        "allocations": [
            {"symbol": "VTI", "weight": 30, "category": "US Equity"},
            {"symbol": "TLT", "weight": 40, "category": "Long-Term Bonds"},
            {"symbol": "IEF", "weight": 15, "category": "Mid-Term Bonds"},
            {"symbol": "GLD", "weight": 7.5, "category": "Gold"},
            {"symbol": "DBC", "weight": 7.5, "category": "Commodities"},
        ],
    },
    "Growth Focus": {
        "description": "Enfocado en crecimiento a largo plazo",
        "risk_level": "Agresivo",
        "allocations": [
            {"symbol": "VTI", "weight": 35, "category": "US Total Market"},
            {"symbol": "QQQ", "weight": 25, "category": "Tech/Growth"},
            {"symbol": "VGT", "weight": 15, "category": "Technology"},
            {"symbol": "VXUS", "weight": 15, "category": "International"},
            {"symbol": "BND", "weight": 10, "category": "Bonds"},
        ],
    },
    "Dividend Income": {
        "description": "Generación de ingresos por dividendos",
        "risk_level": "Moderado",
        "allocations": [
            {"symbol": "VYM", "weight": 25, "category": "High Dividend"},
            {"symbol": "SCHD", "weight": 25, "category": "Dividend Growth"},
            {"symbol": "VNQ", "weight": 15, "category": "REITs"},
            {"symbol": "BND", "weight": 20, "category": "Bonds"},
            {"symbol": "VXUS", "weight": 15, "category": "International"},
        ],
    },
    "Tech Heavy": {
        "description": "Alta exposición a tecnología",
        "risk_level": "Muy Agresivo",
        "allocations": [
            {"symbol": "QQQ", "weight": 35, "category": "Nasdaq 100"},
            {"symbol": "VGT", "weight": 25, "category": "Technology"},
            {"symbol": "SMH", "weight": 15, "category": "Semiconductors"},
            {"symbol": "ARKK", "weight": 10, "category": "Innovation"},
            {"symbol": "VTI", "weight": 15, "category": "US Total Market"},
        ],
    },
    "Conservative Income": {
        "description": "Máxima preservación con ingresos",
        "risk_level": "Conservador",
        "allocations": [
            {"symbol": "BND", "weight": 35, "category": "US Bonds"},
            {"symbol": "VCSH", "weight": 20, "category": "Short-Term Corp"},
            {"symbol": "VYM", "weight": 20, "category": "Dividend Equity"},
            {"symbol": "VGSH", "weight": 15, "category": "Short-Term Treasury"},
            {"symbol": "VTIP", "weight": 10, "category": "TIPS"},
        ],
    },
    "ESG Sustainable": {
        "description": "Inversión responsable y sostenible",
        "risk_level": "Moderado",
        "allocations": [
            {"symbol": "ESGU", "weight": 35, "category": "ESG US Equity"},
            {"symbol": "ESGV", "weight": 20, "category": "ESG US Stock"},
            {"symbol": "ICLN", "weight": 15, "category": "Clean Energy"},
            {"symbol": "EAGG", "weight": 20, "category": "ESG Bonds"},
            {"symbol": "VSGX", "weight": 10, "category": "ESG International"},
        ],
    },
}


def get_risk_profiles() -> Dict:
    """Retorna los perfiles de riesgo disponibles."""
    return RISK_PROFILES


def get_investment_horizons() -> Dict:
    """Retorna los horizontes de inversión disponibles."""
    return INVESTMENT_HORIZONS


def get_portfolio_templates() -> Dict:
    """Retorna los templates de portafolio disponibles."""
    return PORTFOLIO_TEMPLATES


def calculate_portfolio_metrics(
    allocations: List[Dict],
    period: str = "1y"
) -> Dict:
    """
    Calcula métricas de un portafolio.

    Args:
        allocations: Lista de {symbol, weight}
        period: Período de análisis

    Returns:
        Dict con métricas del portafolio
    """
    try:
        symbols = [a["symbol"] for a in allocations]
        weights = np.array([a["weight"] / 100 for a in allocations])

        # Descargar datos
        data = yf.download(symbols, period=period, progress=False)['Close']

        if data.empty:
            return {"error": "No se pudieron obtener datos"}

        # Calcular retornos
        returns = data.pct_change().dropna()

        # Retorno del portafolio
        portfolio_returns = (returns * weights).sum(axis=1)

        # Métricas
        annual_return = (1 + portfolio_returns.mean()) ** 252 - 1
        volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0

        # Drawdown máximo
        cumulative = (1 + portfolio_returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        # Beta vs SPY
        try:
            spy = yf.download("SPY", period=period, progress=False)['Close']
            spy_returns = spy.pct_change().dropna()
            # Alinear fechas
            common_dates = portfolio_returns.index.intersection(spy_returns.index)
            if len(common_dates) > 30:
                port_aligned = portfolio_returns.loc[common_dates]
                spy_aligned = spy_returns.loc[common_dates]
                covariance = np.cov(port_aligned, spy_aligned)[0, 1]
                spy_variance = np.var(spy_aligned)
                beta = covariance / spy_variance if spy_variance > 0 else 1.0
            else:
                beta = 1.0
        except:
            beta = 1.0

        # Correlación promedio entre activos
        corr_matrix = returns.corr()
        avg_correlation = corr_matrix.values[np.triu_indices_from(corr_matrix.values, 1)].mean()

        return {
            "annual_return": annual_return * 100,
            "volatility": volatility * 100,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_drawdown * 100,
            "beta": beta,
            "avg_correlation": avg_correlation,
            "total_return": (cumulative.iloc[-1] - 1) * 100,
        }
    except Exception as e:
        return {"error": str(e)}


def generate_custom_portfolio(
    risk_profile: str,
    horizon: str,
    amount: float,
    preferences: Optional[Dict] = None
) -> Dict:
    """
    Genera un portafolio personalizado basado en parámetros.

    Args:
        risk_profile: Perfil de riesgo del inversor
        horizon: Horizonte de inversión
        amount: Monto a invertir
        preferences: Preferencias adicionales (sectores, ESG, etc.)

    Returns:
        Dict con portafolio generado
    """
    profile = RISK_PROFILES.get(risk_profile, RISK_PROFILES["Moderado"])
    horizon_data = INVESTMENT_HORIZONS.get(horizon, INVESTMENT_HORIZONS["Mediano Plazo (3-7 años)"])

    # Ajustar rangos por horizonte
    equity_min = max(0, profile["equity_range"][0] + horizon_data["equity_adjustment"])
    equity_max = min(100, profile["equity_range"][1] + horizon_data["equity_adjustment"])
    equity_target = (equity_min + equity_max) / 2

    bond_min = max(0, profile["bond_range"][0] + horizon_data["bond_adjustment"])
    bond_max = min(100, profile["bond_range"][1] + horizon_data["bond_adjustment"])
    bond_target = (bond_min + bond_max) / 2

    alt_target = (profile["alternative_range"][0] + profile["alternative_range"][1]) / 2

    # Normalizar a 100%
    total = equity_target + bond_target + alt_target
    equity_pct = (equity_target / total) * 100
    bond_pct = (bond_target / total) * 100
    alt_pct = (alt_target / total) * 100

    # Construir portafolio
    allocations = []

    # Equity allocation
    if equity_pct > 50:
        allocations.append({"symbol": "VTI", "weight": equity_pct * 0.5, "category": "US Total Market"})
        allocations.append({"symbol": "VXUS", "weight": equity_pct * 0.3, "category": "International"})
        allocations.append({"symbol": "QQQ", "weight": equity_pct * 0.2, "category": "Growth"})
    elif equity_pct > 30:
        allocations.append({"symbol": "VTI", "weight": equity_pct * 0.6, "category": "US Total Market"})
        allocations.append({"symbol": "VXUS", "weight": equity_pct * 0.4, "category": "International"})
    else:
        allocations.append({"symbol": "VTI", "weight": equity_pct * 0.7, "category": "US Total Market"})
        allocations.append({"symbol": "VYM", "weight": equity_pct * 0.3, "category": "Dividend"})

    # Bond allocation
    if bond_pct > 30:
        allocations.append({"symbol": "BND", "weight": bond_pct * 0.6, "category": "Total Bond"})
        allocations.append({"symbol": "VCSH", "weight": bond_pct * 0.4, "category": "Short-Term Corp"})
    elif bond_pct > 10:
        allocations.append({"symbol": "BND", "weight": bond_pct, "category": "Total Bond"})
    else:
        allocations.append({"symbol": "VGSH", "weight": bond_pct, "category": "Short-Term Treasury"})

    # Alternative allocation
    if alt_pct > 5:
        allocations.append({"symbol": "GLD", "weight": alt_pct * 0.6, "category": "Gold"})
        allocations.append({"symbol": "VNQ", "weight": alt_pct * 0.4, "category": "Real Estate"})
    elif alt_pct > 0:
        allocations.append({"symbol": "GLD", "weight": alt_pct, "category": "Gold"})

    # Normalizar pesos a 100%
    total_weight = sum(a["weight"] for a in allocations)
    for a in allocations:
        a["weight"] = round(a["weight"] / total_weight * 100, 1)
        a["amount"] = round(amount * a["weight"] / 100, 2)

    # Calcular métricas
    metrics = calculate_portfolio_metrics(allocations)

    return {
        "allocations": allocations,
        "metrics": metrics,
        "risk_profile": risk_profile,
        "horizon": horizon,
        "total_amount": amount,
        "equity_pct": round(equity_pct, 1),
        "bond_pct": round(bond_pct, 1),
        "alternative_pct": round(alt_pct, 1),
    }


def get_ai_portfolio_recommendation(
    risk_profile: str,
    horizon: str,
    amount: float,
    goals: str,
    constraints: str,
    api_key: Optional[str] = None
) -> Dict:
    """
    Genera recomendación de portafolio usando IA.

    Args:
        risk_profile: Perfil de riesgo
        horizon: Horizonte de inversión
        amount: Monto a invertir
        goals: Objetivos del inversor
        constraints: Restricciones o preferencias
        api_key: API key de Anthropic

    Returns:
        Dict con allocations y rationale
    """
    if api_key is None:
        return get_fallback_recommendation(risk_profile, horizon, amount)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        profile_info = RISK_PROFILES.get(risk_profile, {})
        horizon_info = INVESTMENT_HORIZONS.get(horizon, {})

        prompt = f"""Eres un asesor financiero experto en construcción de portafolios.

**PERFIL DEL INVERSOR:**
- Perfil de Riesgo: {risk_profile}
  - Descripción: {profile_info.get('description', '')}
  - Volatilidad objetivo: {profile_info.get('target_volatility', 12)}%
- Horizonte: {horizon}
  - Enfoque: {horizon_info.get('focus', '')}
- Monto a Invertir: ${amount:,.2f}

**OBJETIVOS DEL INVERSOR:**
{goals if goals else 'Crecimiento general del capital'}

**RESTRICCIONES/PREFERENCIAS:**
{constraints if constraints else 'Sin restricciones específicas'}

**ETFs DISPONIBLES PARA RECOMENDAR:**
- Equity US: VTI, VOO, QQQ, VUG, VTV, SCHD, VYM
- International: VXUS, VEA, VWO, EFA, EEM
- Bonds: BND, AGG, TLT, IEF, VCSH, VGSH
- Sectors: VGT, XLK, XLV, XLF, VNQ
- Alternatives: GLD, IAU, DBC, PDBC

IMPORTANTE: Tu respuesta DEBE seguir EXACTAMENTE este formato JSON:
{{
  "allocations": [
    {{"symbol": "VTI", "weight": 40, "category": "US Equity"}},
    {{"symbol": "VXUS", "weight": 20, "category": "International"}}
  ],
  "rationale": "Explicación breve de la recomendación en 2-3 oraciones."
}}

Reglas:
- Los weights deben sumar 100
- Usa solo ETFs de la lista proporcionada
- El rationale debe ser conciso (máximo 150 palabras)
- Responde SOLO con el JSON, sin texto adicional"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text.strip()

        # Intentar parsear JSON
        import json
        try:
            # Limpiar respuesta si tiene markdown
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            # Si falla el parsing, usar fallback
            return get_fallback_recommendation(risk_profile, horizon, amount)

    except ImportError:
        return get_fallback_recommendation(risk_profile, horizon, amount)
    except Exception as e:
        print(f"Error en recomendación IA: {e}")
        return get_fallback_recommendation(risk_profile, horizon, amount)


def get_fallback_recommendation(
    risk_profile: str,
    horizon: str,
    amount: float
) -> Dict:
    """Genera recomendación básica sin IA."""

    # Seleccionar template basado en perfil
    template_map = {
        "Conservador": "Conservative Income",
        "Moderado": "Classic 60/40",
        "Agresivo": "Growth Focus",
        "Muy Agresivo": "Tech Heavy",
    }

    template_name = template_map.get(risk_profile, "Classic 60/40")
    template = PORTFOLIO_TEMPLATES.get(template_name, PORTFOLIO_TEMPLATES["Classic 60/40"])

    rationale = f"""Portafolio {template_name}: {template['description']}.
Nivel de riesgo: {template['risk_level']}.
Recomendaciones: Rebalancear cada 6-12 meses, mantener costos bajos con ETFs, considerar implicaciones fiscales.
Nota: Consulta con un asesor financiero certificado antes de invertir."""

    return {
        "allocations": template["allocations"],
        "rationale": rationale
    }


def backtest_portfolio(
    allocations: List[Dict],
    years: int = 5
) -> Dict:
    """
    Realiza backtest de un portafolio.

    Args:
        allocations: Lista de {symbol, weight}
        years: Años de backtest

    Returns:
        Dict con resultados del backtest
    """
    try:
        symbols = [a["symbol"] for a in allocations]
        weights = np.array([a["weight"] / 100 for a in allocations])

        # Descargar datos históricos
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)

        data = yf.download(symbols, start=start_date, end=end_date, progress=False)['Close']

        if data.empty:
            return {"error": "No se pudieron obtener datos históricos"}

        # Calcular retornos diarios
        returns = data.pct_change().dropna()

        # Portafolio returns
        portfolio_returns = (returns * weights).sum(axis=1)

        # Serie de valor del portafolio (empezando en 10000)
        portfolio_value = (1 + portfolio_returns).cumprod() * 10000

        # Métricas anuales (usar 'Y' para compatibilidad con pandas < 2.2)
        try:
            yearly_returns = portfolio_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)
        except ValueError:
            yearly_returns = portfolio_returns.resample('Y').apply(lambda x: (1 + x).prod() - 1)

        # Mejor y peor año
        best_year = yearly_returns.max() * 100
        worst_year = yearly_returns.min() * 100

        # Drawdowns
        rolling_max = portfolio_value.expanding().max()
        drawdowns = (portfolio_value - rolling_max) / rolling_max
        max_drawdown = drawdowns.min() * 100

        # Sharpe anualizado
        annual_return = (1 + portfolio_returns.mean()) ** 252 - 1
        annual_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe = annual_return / annual_vol if annual_vol > 0 else 0

        return {
            "start_date": data.index[0].strftime("%Y-%m-%d"),
            "end_date": data.index[-1].strftime("%Y-%m-%d"),
            "initial_value": 10000,
            "final_value": portfolio_value.iloc[-1],
            "total_return": (portfolio_value.iloc[-1] / 10000 - 1) * 100,
            "cagr": ((portfolio_value.iloc[-1] / 10000) ** (1 / years) - 1) * 100,
            "volatility": annual_vol * 100,
            "sharpe_ratio": sharpe,
            "max_drawdown": max_drawdown,
            "best_year": best_year,
            "worst_year": worst_year,
            "positive_years": (yearly_returns > 0).sum(),
            "total_years": len(yearly_returns),
            "portfolio_values": portfolio_value.to_dict(),
        }
    except Exception as e:
        return {"error": str(e)}


def optimize_portfolio(
    symbols: List[str],
    target_return: Optional[float] = None,
    max_volatility: Optional[float] = None
) -> Dict:
    """
    Optimiza un portafolio usando Mean-Variance Optimization simplificada.

    Args:
        symbols: Lista de símbolos
        target_return: Retorno objetivo anual (%)
        max_volatility: Volatilidad máxima (%)

    Returns:
        Dict con pesos optimizados
    """
    try:
        # Descargar datos
        data = yf.download(symbols, period="2y", progress=False)['Close']

        if data.empty:
            return {"error": "No se pudieron obtener datos"}

        returns = data.pct_change().dropna()

        # Calcular retornos esperados y matriz de covarianza
        expected_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252

        n_assets = len(symbols)

        # Optimización simple: maximizar Sharpe
        best_sharpe = -np.inf
        best_weights = None

        # Monte Carlo para encontrar mejor combinación
        for _ in range(10000):
            weights = np.random.random(n_assets)
            weights /= weights.sum()

            port_return = np.dot(weights, expected_returns)
            port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe = port_return / port_vol if port_vol > 0 else 0

            # Aplicar restricciones si existen
            if target_return and port_return * 100 < target_return:
                continue
            if max_volatility and port_vol * 100 > max_volatility:
                continue

            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_weights = weights

        if best_weights is None:
            # Si no se encontró solución, usar equal weight
            best_weights = np.ones(n_assets) / n_assets

        # Construir resultado
        allocations = [
            {"symbol": symbols[i], "weight": round(best_weights[i] * 100, 1)}
            for i in range(n_assets)
        ]

        port_return = np.dot(best_weights, expected_returns) * 100
        port_vol = np.sqrt(np.dot(best_weights.T, np.dot(cov_matrix, best_weights))) * 100

        return {
            "allocations": allocations,
            "expected_return": port_return,
            "expected_volatility": port_vol,
            "sharpe_ratio": best_sharpe,
        }
    except Exception as e:
        return {"error": str(e)}
