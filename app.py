import gradio as gr
from agentes.agente_financiero import obtener_datos_financieros
from agentes.agente_sentimiento import analizar_sentimiento

def analizar_accion(ticker):
    datos_financieros = obtener_datos_financieros(ticker)
    datos_sentimiento = analizar_sentimiento(ticker)
    informe = f"{datos_financieros}\n\n{datos_sentimiento}"
    return informe

app = gr.Interface(
    fn=analizar_accion,
    inputs=gr.Textbox(label="Ticker de la acción (ejemplo: AAPL)"),
    outputs=gr.Textbox(label="Informe generado"),
    title="Análisis de Bolsa con Agentes de IA",
    description="Introduce el ticker de una acción para generar un informe de análisis financiero y de sentimiento"
)

app.launch()
