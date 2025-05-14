import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from yahooquery import Ticker as YahooTicker
import os

# === MÉTODO 1: YFINANCE ===
def obtener_datos_yfinance(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="1y")

        if hist.empty:
            return "No se encontraron datos financieros para este ticker."

        rentabilidad_1y = (hist['Close'][-1] / hist['Close'][0] - 1) * 100
        rentabilidad_1m = (hist['Close'][-1] / hist['Close'][-22] - 1) * 100
        media_50 = hist['Close'][-50:].mean()
        tendencia = "Alcista" if hist['Close'][-1] > media_50 else "Bajista"
        volatilidad = hist['Close'].pct_change().std() * (252 ** 0.5)

        if volatilidad < 0.2:
            nivel_volatilidad = "Baja"
        elif volatilidad < 0.4:
            nivel_volatilidad = "Media"
        else:
            nivel_volatilidad = "Alta"

        return (
            f"🔹 Rentabilidad 1 año: {rentabilidad_1y:.2f}%\n"
            f"🔹 Rentabilidad 1 mes: {rentabilidad_1m:.2f}%\n"
            f"🔹 Tendencia actual: {tendencia}\n"
            f"🔹 Volatilidad: {nivel_volatilidad}"
        )

    except Exception as e:
        return f"Error con yfinance: {str(e)}"

# === MÉTODO 2: ALPHA VANTAGE ===
def obtener_datos_alpha_vantage(ticker):
    try:
        # Reemplaza con tu propia API key
        ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY") or "76HG02Y71T8E4YUD"
        ts = TimeSeries(key=ALPHA_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=ticker, outputsize='compact')

        if data.empty:
            return "No se encontraron datos con Alpha Vantage."

        data.sort_index(inplace=True)
        cierre = data['4. close']
        rentabilidad_1y = (cierre.iloc[-1] / cierre.iloc[0] - 1) * 100
        rentabilidad_1m = (cierre.iloc[-1] / cierre.iloc[-22] - 1) * 100
        media_50 = cierre[-50:].mean()
        tendencia = "Alcista" if cierre.iloc[-1] > media_50 else "Bajista"
        volatilidad = cierre.pct_change().std() * (252 ** 0.5)

        if volatilidad < 0.2:
            nivel_volatilidad = "Baja"
        elif volatilidad < 0.4:
            nivel_volatilidad = "Media"
        else:
            nivel_volatilidad = "Alta"

        return (
            f"🔹 Rentabilidad 1 año: {rentabilidad_1y:.2f}%\n"
            f"🔹 Rentabilidad 1 mes: {rentabilidad_1m:.2f}%\n"
            f"🔹 Tendencia actual: {tendencia}\n"
            f"🔹 Volatilidad: {nivel_volatilidad}"
        )

    except Exception as e:
        return f"Error con Alpha Vantage: {str(e)}"

# === MÉTODO 3: YAHOOQUERY ===
def obtener_datos_yahooquery(ticker):
    try:
        t = YahooTicker(ticker)
        hist = t.history(period="1y", interval="1d")

        if hist.empty:
            return "No se encontraron datos con YahooQuery."

        df = hist.reset_index()
        cierre = df["close"]
        rentabilidad_1y = (cierre.iloc[-1] / cierre.iloc[0] - 1) * 100
        rentabilidad_1m = (cierre.iloc[-1] / cierre.iloc[-22] - 1) * 100
        media_50 = cierre[-50:].mean()
        tendencia = "Alcista" if cierre.iloc[-1] > media_50 else "Bajista"
        volatilidad = cierre.pct_change().std() * (252 ** 0.5)

        if volatilidad < 0.2:
            nivel_volatilidad = "Baja"
        elif volatilidad < 0.4:
            nivel_volatilidad = "Media"
        else:
            nivel_volatilidad = "Alta"

        return (
            f"🔹 Rentabilidad 1 año: {rentabilidad_1y:.2f}%\n"
            f"🔹 Rentabilidad 1 mes: {rentabilidad_1m:.2f}%\n"
            f"🔹 Tendencia actual: {tendencia}\n"
            f"🔹 Volatilidad: {nivel_volatilidad}"
        )

    except Exception as e:
        return f"Error con YahooQuery: {str(e)}"

# === INTELIGENTE: PROBAR LOS TRES ===
def obtener_datos_financieros(ticker):
    for metodo in [obtener_datos_yfinance, obtener_datos_alpha_vantage, obtener_datos_yahooquery]:
        resultado = metodo(ticker)
        if "Error" not in resultado and "No se encontraron" not in resultado:
            return resultado
    return "❌ No se pudo obtener información financiera con ninguna fuente."
