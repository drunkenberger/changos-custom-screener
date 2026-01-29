"""
Glosario Financiero para el Dashboard
Términos técnicos con definiciones y ejemplos
"""

GLOSSARY_TERMS = {
    "Perfil": [
        {
            "term": "Market Cap",
            "definition": "Capitalización de mercado. El valor total de todas las acciones en circulación. Precio x Acciones.",
            "example": "100M acciones a $50 = Market Cap de $5B"
        },
        {
            "term": "Beta",
            "definition": "Volatilidad relativa al mercado. Beta 1 = igual al mercado, >1 = más volátil, <1 = menos volátil.",
            "example": "Beta 1.5: si mercado sube 10%, la acción sube ~15%"
        },
        {
            "term": "Earnings Date",
            "definition": "Fecha del reporte de ganancias trimestrales. Suele generar alta volatilidad.",
            "example": "Earnings el 15 de enero = esperar movimiento fuerte ese día"
        },
        {
            "term": "Shares Outstanding",
            "definition": "Total de acciones emitidas en manos de todos los accionistas.",
            "example": "Apple tiene ~15.5 mil millones de acciones"
        },
        {
            "term": "Float (Shares Float)",
            "definition": "Acciones disponibles para trading público. Excluye acciones de insiders con restricciones.",
            "example": "100M outstanding - 20M insiders = 80M float"
        },
        {
            "term": "Short Interest",
            "definition": "Acciones vendidas en corto que no han sido cubiertas. Apuestas bajistas abiertas.",
            "example": "10M de short interest = 10M acciones vendidas en corto"
        },
        {
            "term": "Short % of Float",
            "definition": "Porcentaje del float vendido en corto. Alto % = sentimiento bajista pero riesgo de squeeze.",
            "example": ">20% se considera muy alto, potencial short squeeze"
        },
        {
            "term": "Institutional Ownership",
            "definition": "% de acciones en manos de fondos mutuos, pensiones, hedge funds.",
            "example": "85% institucional = fuerte respaldo profesional"
        },
        {
            "term": "Insider Ownership",
            "definition": "% de acciones en manos de ejecutivos y directores.",
            "example": "15% insider = gerencia alineada con accionistas"
        },
    ],
    "Volume Profile": [
        {
            "term": "POC (Point of Control)",
            "definition": "Nivel de precio con mayor volumen negociado. Actúa como soporte/resistencia clave.",
            "example": "POC en $150 = nivel donde hubo más actividad, precio tiende a ser atraído ahí"
        },
        {
            "term": "VAH (Value Area High)",
            "definition": "Límite superior del área donde se negoció 70% del volumen. Resistencia.",
            "example": "VAH en $155 actúa como resistencia. Romperlo = señal alcista"
        },
        {
            "term": "VAL (Value Area Low)",
            "definition": "Límite inferior del área donde se negoció 70% del volumen. Soporte.",
            "example": "VAL en $145 actúa como soporte. Perderlo = señal bajista"
        },
    ],
    "Indicadores Técnicos": [
        {
            "term": "EMA (Exponential Moving Average)",
            "definition": "Media móvil que da más peso a precios recientes. EMA 20/50/100/200 son las más usadas.",
            "example": "Precio > EMAs = alcista. EMA 20 corta EMA 50 al alza = golden cross"
        },
        {
            "term": "VWAP",
            "definition": "Precio promedio ponderado por volumen. Referencia institucional.",
            "example": "Precio > VWAP = compradores en control. < VWAP = vendedores"
        },
        {
            "term": "RSI (Relative Strength Index)",
            "definition": "Oscilador 0-100. >70 = sobrecompra, <30 = sobreventa.",
            "example": "RSI 75 = sobrecompra, posible corrección. RSI 25 = sobreventa, posible rebote"
        },
        {
            "term": "MACD",
            "definition": "Diferencia entre EMA 12 y 26. Señales cuando cruza línea de señal.",
            "example": "MACD cruza arriba de señal = compra. Cruza abajo = venta"
        },
        {
            "term": "Bullish Divergence",
            "definition": "Precio hace mínimo más bajo, RSI hace mínimo más alto. Señal de reversión alcista.",
            "example": "Precio baja $50→$45, RSI sube 25→30 = vendedores agotándose"
        },
        {
            "term": "Bearish Divergence",
            "definition": "Precio hace máximo más alto, RSI hace máximo más bajo. Señal de reversión bajista.",
            "example": "Precio sube $100→$110, RSI baja 75→65 = momentum debilitándose"
        },
        {
            "term": "Overbought (Sobrecompra)",
            "definition": "RSI > 70. Activo subió muy rápido, posible corrección.",
            "example": "RSI 80 después de +20% = toma de ganancias probable"
        },
        {
            "term": "Oversold (Sobreventa)",
            "definition": "RSI < 30. Activo cayó muy rápido, posible rebote.",
            "example": "RSI 20 después de -25% = rebote probable"
        },
        {
            "term": "ATR (Average True Range)",
            "definition": "Volatilidad promedio diaria. Útil para calcular stop-loss.",
            "example": "ATR $2.50 = movimiento típico de $2.50/día. SL = 1.5x ATR"
        },
        {
            "term": "Momentum",
            "definition": "Fuerza y dirección del precio. Combina RSI, MACD y posición vs EMAs.",
            "example": "FULLY BULLISH = RSI alto + MACD positivo + precio > EMAs"
        },
    ],
    "Precios": [
        {
            "term": "Open",
            "definition": "Precio de apertura del mercado.",
            "example": "Close ayer $50, Open hoy $52 = gap up de $2"
        },
        {
            "term": "High",
            "definition": "Precio máximo del período.",
            "example": "High $55 = máximo alcanzado ese día"
        },
        {
            "term": "Low",
            "definition": "Precio mínimo del período.",
            "example": "Low $48 = mínimo del día. Rango = High - Low"
        },
        {
            "term": "Close",
            "definition": "Precio de cierre. El más importante para análisis técnico.",
            "example": "Close cerca de High = fortaleza. Close cerca de Low = debilidad"
        },
        {
            "term": "Volume",
            "definition": "Acciones negociadas. Alto volumen confirma movimientos.",
            "example": "Breakout con 5x volumen promedio = movimiento confiable"
        },
    ],
    "Opciones": [
        {
            "term": "Strike",
            "definition": "Precio de ejercicio de la opción.",
            "example": "Call strike $50 = derecho a comprar a $50"
        },
        {
            "term": "Call",
            "definition": "Opción de compra. Ganas si el precio sube.",
            "example": "Call $50 por $2, acción sube a $60 = ganas $8"
        },
        {
            "term": "Put",
            "definition": "Opción de venta. Ganas si el precio baja.",
            "example": "Put $50 por $2, acción baja a $40 = ganas $8"
        },
        {
            "term": "Expiration",
            "definition": "Fecha de vencimiento. Después, la opción no vale nada.",
            "example": "Expiración 19 enero = ejercer o vender antes de esa fecha"
        },
        {
            "term": "Bid/Ask",
            "definition": "Bid = precio de compra. Ask = precio de venta. Spread = diferencia.",
            "example": "Bid $2.50, Ask $2.60 = spread de $0.10"
        },
        {
            "term": "Open Interest (OI)",
            "definition": "Contratos abiertos no cerrados. Alto OI = mucho interés en ese strike.",
            "example": "OI 50,000 en strike $150 = nivel importante"
        },
        {
            "term": "Implied Volatility (IV)",
            "definition": "Expectativa de movimiento futuro. IV alta = opciones caras.",
            "example": "IV 80% antes de earnings = mercado espera movimiento grande"
        },
    ],
    "Estados Financieros": [
        {
            "term": "Revenue (Ingresos)",
            "definition": "Ventas totales antes de costos. 'Top line'.",
            "example": "$100B en ventas de productos y servicios"
        },
        {
            "term": "Gross Profit",
            "definition": "Revenue - Costo de productos (COGS).",
            "example": "Revenue $100M - COGS $60M = Gross Profit $40M"
        },
        {
            "term": "Operating Income",
            "definition": "Gross Profit - Gastos operativos. Rentabilidad del negocio principal.",
            "example": "Gross $40M - OpEx $25M = Operating Income $15M"
        },
        {
            "term": "EBITDA",
            "definition": "Ganancias antes de intereses, impuestos, depreciación y amortización.",
            "example": "Mejor proxy de flujo de efectivo operativo que Net Income"
        },
        {
            "term": "Net Income",
            "definition": "Ganancia final después de todo. 'Bottom line'.",
            "example": "Lo que queda para accionistas o reinversión"
        },
        {
            "term": "Operating Cash Flow (OCF)",
            "definition": "Efectivo generado por operaciones. Más confiable que Net Income.",
            "example": "OCF > Net Income = ganancias respaldadas por efectivo"
        },
        {
            "term": "CapEx",
            "definition": "Gastos en activos físicos (equipos, edificios, tecnología).",
            "example": "CapEx $30M = inversión en infraestructura"
        },
        {
            "term": "Free Cash Flow (FCF)",
            "definition": "OCF - CapEx. Efectivo libre para dividendos, buybacks o pagar deuda.",
            "example": "OCF $80M - CapEx $30M = FCF $50M"
        },
    ],
    "Valoración": [
        {
            "term": "P/E Ratio",
            "definition": "Precio / Ganancias por acción. Cuánto pagas por $1 de ganancias.",
            "example": "P/E 20 = pagas $20 por $1 de EPS. <15 barato, >30 caro (depende sector)"
        },
        {
            "term": "Forward P/E",
            "definition": "P/E con ganancias estimadas futuras.",
            "example": "P/E actual 25, Forward P/E 18 = crecimiento esperado"
        },
        {
            "term": "PEG Ratio",
            "definition": "P/E dividido por tasa de crecimiento. <1 puede ser subvaluado.",
            "example": "P/E 30, crecimiento 30% = PEG 1 (fair). Crecimiento 15% = PEG 2 (caro)"
        },
        {
            "term": "P/S (Price to Sales)",
            "definition": "Precio / Ventas por acción. Útil para empresas sin ganancias.",
            "example": "P/S 5 = pagas $5 por $1 de ventas"
        },
        {
            "term": "P/B (Price to Book)",
            "definition": "Precio / Valor en libros. Compara precio de mercado vs contable.",
            "example": "P/B 1.5 = pagas 50% más que valor contable. <1 puede ser ganga"
        },
        {
            "term": "EV/EBITDA",
            "definition": "Enterprise Value / EBITDA. Considera deuda, más completo que P/E.",
            "example": "EV/EBITDA 10 = empresa vale 10x su EBITDA"
        },
        {
            "term": "EPS",
            "definition": "Ganancias por acción. Net Income / Acciones.",
            "example": "Net Income $1B / 100M acciones = EPS $10"
        },
    ],
    "Rentabilidad": [
        {
            "term": "ROE (Return on Equity)",
            "definition": "Net Income / Equity. Retorno sobre capital de accionistas.",
            "example": "ROE 20% = $20 de ganancia por $100 de equity. >15% es bueno"
        },
        {
            "term": "ROA (Return on Assets)",
            "definition": "Net Income / Total Assets. Eficiencia de uso de activos.",
            "example": "ROA 8% = $8 de ganancia por $100 de activos"
        },
        {
            "term": "Gross Margin",
            "definition": "Gross Profit / Revenue. Margen después de costos directos.",
            "example": "Margen bruto 40% = $40 de cada $100 vendidos es ganancia bruta"
        },
        {
            "term": "Operating Margin",
            "definition": "Operating Income / Revenue. Eficiencia operacional.",
            "example": "Margen operativo 20% = buen control de costos"
        },
        {
            "term": "Net Margin",
            "definition": "Net Income / Revenue. Ganancia final por cada $1 de ventas.",
            "example": "Margen neto 10% = $10 de cada $100 es ganancia neta"
        },
    ],
    "Deuda y Liquidez": [
        {
            "term": "Debt to Equity (D/E)",
            "definition": "Deuda / Equity. Mide apalancamiento financiero.",
            "example": "D/E 0.5 = conservador. D/E 2 = agresivo"
        },
        {
            "term": "Current Ratio",
            "definition": "Activos corrientes / Pasivos corrientes. Capacidad de pagar deudas corto plazo.",
            "example": "Current Ratio 2 = $2 de activos por $1 de deuda. >1.5 es saludable"
        },
        {
            "term": "Quick Ratio",
            "definition": "Como Current Ratio pero sin inventario. Más conservador.",
            "example": "Quick Ratio 1.2 = puede pagar deudas sin vender inventario"
        },
        {
            "term": "Interest Coverage",
            "definition": "EBIT / Gastos de intereses. Capacidad de pagar intereses.",
            "example": "Coverage 5x = ganancias son 5 veces los pagos de interés"
        },
    ],
    "Dividendos": [
        {
            "term": "Dividend Yield",
            "definition": "Dividendo anual / Precio. Retorno por mantener la acción.",
            "example": "Yield 3% en acción de $100 = $3/año en dividendos"
        },
        {
            "term": "Payout Ratio",
            "definition": "% de ganancias pagado como dividendos.",
            "example": "Payout 40% = 40% de ganancias a dividendos, 60% retienen"
        },
    ],
    "Trading": [
        {
            "term": "Stop Loss (SL)",
            "definition": "Orden para vender si precio baja a cierto nivel. Limita pérdidas.",
            "example": "Compras $100, SL $95 = pérdida máxima 5%"
        },
        {
            "term": "Take Profit (TP)",
            "definition": "Orden para vender cuando llegas a tu objetivo de ganancia.",
            "example": "Compras $100, TP $120 = aseguras +20%"
        },
        {
            "term": "Risk/Reward (R/R)",
            "definition": "Lo que arriesgas vs lo que puedes ganar. Mínimo 1:2 recomendado.",
            "example": "Arriesgas $5 para ganar $15 = R/R 1:3"
        },
        {
            "term": "Position Size",
            "definition": "Cuántas acciones comprar según tu riesgo por operación.",
            "example": "Capital $25K, riesgo 2% ($500), SL $5/acción = 100 acciones"
        },
    ],
}


def get_glossary_html():
    """Generate HTML for the glossary popup/expander."""
    html = ""
    for category, terms in GLOSSARY_TERMS.items():
        html += f'<div style="margin-bottom:20px;"><h4 style="color:#FF00FF;font-family:Bebas Neue,sans-serif;font-size:1.1rem;border-bottom:2px solid #FF00FF;padding-bottom:5px;margin-bottom:10px;">{category}</h4>'
        for t in terms:
            html += f'''
            <div style="background:rgba(26,26,46,0.8);border-left:3px solid #00FFFF;padding:8px 12px;margin-bottom:8px;">
                <div style="color:#00FFFF;font-weight:bold;font-size:0.9rem;">{t["term"]}</div>
                <div style="color:#E0E0E0;font-size:0.8rem;margin-top:3px;">{t["definition"]}</div>
                <div style="color:#888;font-size:0.75rem;margin-top:3px;font-style:italic;">Ej: {t["example"]}</div>
            </div>
            '''
        html += '</div>'
    return html
