import os
import matplotlib.pyplot as plt
import yfinance as yf
from yahooquery import Ticker as YahooTicker
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import shutil

def limpiar_imagenes():
    carpeta = "img"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    else:
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".png"):
                os.remove(os.path.join(carpeta, archivo))


# Tu API Key de Alpha Vantage (usa variable de entorno o ponla directa)
ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY") or "76HG02Y71T8E4YUD"

def descargar_datos_yfinance(ticker):
    try:
        data = yf.download(ticker, period="6mo", interval="1d", auto_adjust=False)
        if data.empty:
            raise Exception("Sin datos")
        return data
    except Exception:
        return None

def descargar_datos_yahooquery(ticker):
    try:
        yt = YahooTicker(ticker)
        hist = yt.history(period="6mo", interval="1d")
        if hist.empty:
            raise Exception("Sin datos")
        df = hist.reset_index()
        df = df[df['symbol'] == ticker]
        df = df.set_index('date')
        df.index = pd.to_datetime(df.index)
        df = df[["open", "high", "low", "close", "volume"]]
        df.columns = [c.capitalize() for c in df.columns]
        return df
    except Exception:
        return None

def descargar_datos_alphavantage(ticker):
    try:
        ts = TimeSeries(key=ALPHA_KEY, output_format='pandas')
        data, _ = ts.get_daily(symbol=ticker, outputsize='compact')
        if data.empty:
            raise Exception("Sin datos")
        data = data.sort_index()
        data = data.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        return data
    except Exception:
        return None

def generar_graficos_multiples(ticker):
    limpiar_imagenes()
    # Intenta obtener los datos desde distintas fuentes
    datos = descargar_datos_yfinance(ticker)
    if datos is None:
        datos = descargar_datos_yahooquery(ticker)
    if datos is None:
        datos = descargar_datos_alphavantage(ticker)
    if datos is None or datos.empty:
        return [], "❌ No se pudieron obtener datos de ninguna fuente."

    rutas = []

    try:
        # 1. Precio de cierre
        plt.figure(figsize=(10, 4))
        plt.plot(datos['Close'], label='Precio de cierre')
        plt.title(f"{ticker.upper()} - Precio de cierre")
        plt.xlabel("Fecha")
        plt.ylabel("USD")
        plt.legend()
        ruta = f"img/grafico1_{ticker}.png"
        plt.tight_layout(); plt.savefig(ruta); plt.close()
        rutas.append(ruta)

        # 2. Precio de apertura
        plt.figure(figsize=(10, 4))
        plt.plot(datos['Open'], label='Precio de apertura', color='orange')
        plt.title(f"{ticker.upper()} - Precio de apertura")
        plt.xlabel("Fecha"); plt.ylabel("USD"); plt.legend()
        ruta = f"img/grafico2_{ticker}.png"
        plt.tight_layout(); plt.savefig(ruta); plt.close()
        rutas.append(ruta)

        # 3. Volumen
        plt.figure(figsize=(10, 4))
        plt.plot(datos['Volume'], label='Volumen', color='green')
        plt.title(f"{ticker.upper()} - Volumen de transacciones")
        plt.xlabel("Fecha"); plt.ylabel("Volumen"); plt.legend()
        ruta = f"img/grafico3_{ticker}.png"
        plt.tight_layout(); plt.savefig(ruta); plt.close()
        rutas.append(ruta)

        # 4. Media móvil 20 y 50
        ma20 = datos['Close'].rolling(window=20).mean()
        ma50 = datos['Close'].rolling(window=50).mean()
        plt.figure(figsize=(10, 4))
        plt.plot(datos['Close'], label='Precio cierre')
        plt.plot(ma20, label='MA 20 días')
        plt.plot(ma50, label='MA 50 días')
        plt.title(f"{ticker.upper()} - Medias móviles")
        plt.xlabel("Fecha"); plt.ylabel("USD"); plt.legend()
        ruta = f"img/grafico4_{ticker}.png"
        plt.tight_layout(); plt.savefig(ruta); plt.close()
        rutas.append(ruta)

        # 5. Rentabilidad acumulada
        rentabilidad = datos['Close'].pct_change().fillna(0).add(1).cumprod()
        plt.figure(figsize=(10, 4))
        plt.plot(rentabilidad, label='Rentabilidad acumulada', color='purple')
        plt.title(f"{ticker.upper()} - Rentabilidad acumulada")
        plt.xlabel("Fecha"); plt.ylabel("Multiplicador"); plt.legend()
        ruta = f"img/grafico5_{ticker}.png"
        plt.tight_layout(); plt.savefig(ruta); plt.close()
        rutas.append(ruta)

        # 6. Rango diario (High - Low)
        rango = datos['High'] - datos['Low']
        plt.figure(figsize=(10, 4))
        plt.plot(rango, label='Rango diario', color='red')
        plt.title(f"{ticker.upper()} - Rango diario")
        plt.xlabel("Fecha"); plt.ylabel("USD"); plt.legend()
        ruta = f"img/grafico6_{ticker}.png"
        plt.tight_layout(); plt.savefig(ruta); plt.close()
        rutas.append(ruta)

        return rutas, None

    except Exception as e:
        return [], f"❌ Error generando gráficos: {str(e)}"
