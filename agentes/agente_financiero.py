import yfinance as yf

def obtener_datos_financieros(ticker):
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="1y")

        if hist.empty:
            return "No se encontraron datos financieros para este ticker."

        # Rentabilidad
        rentabilidad_1y = (hist['Close'][-1] / hist['Close'][0] - 1) * 100
        rentabilidad_1m = (hist['Close'][-1] / hist['Close'][-22] - 1) * 100  # 22 días ~ 1 mes bursátil

        # Tendencia
        media_50 = hist['Close'][-50:].mean()
        tendencia = "Alcista" if hist['Close'][-1] > media_50 else "Bajista"

        # Volatilidad
        volatilidad = hist['Close'].pct_change().std() * (252 ** 0.5)  # Volatilidad anualizada
        if volatilidad < 0.2:
            nivel_volatilidad = "Baja"
        elif volatilidad < 0.4:
            nivel_volatilidad = "Media"
        else:
            nivel_volatilidad = "Alta"

        resumen = (
            f"🔹 Rentabilidad 1 año: {rentabilidad_1y:.2f}%\n"
            f"🔹 Rentabilidad 1 mes: {rentabilidad_1m:.2f}%\n"
            f"🔹 Tendencia actual: {tendencia}\n"
            f"🔹 Volatilidad: {nivel_volatilidad}"
        )

        return resumen

    except Exception as e:
        return f"Error al obtener datos financieros: {str(e)}"
