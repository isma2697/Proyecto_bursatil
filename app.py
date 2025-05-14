import gradio as gr
from agentes.agente_financiero import obtener_datos_financieros
from agentes.agente_sentimiento import analizar_sentimiento
from agentes.agente_analista import generar_informe
from agentes.agente_grafico import generar_graficos_multiples


TICKERS = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]


def analizar_accion(ticker):
    datos_financieros = obtener_datos_financieros(ticker)
    datos_sentimiento = analizar_sentimiento(ticker)
    informe = generar_informe(datos_financieros, datos_sentimiento)
    rutas_graficos, _ = generar_graficos_multiples(ticker)
    return informe, rutas_graficos



with gr.Blocks(title="Análisis IA de Bolsa") as app:
    gr.Markdown("# 📊 Análisis de Bolsa con Agentes de IA")
    gr.Markdown("Selecciona un ticker para generar el informe:")

    with gr.Row():
        ticker_input = gr.Dropdown(
            choices=TICKERS,
            label="Selecciona o escribe un ticker",
            value="AAPL",
            allow_custom_value=True,  # 👈 esto permite escribir nuevos valores
            scale=3
        )
        boton = gr.Button("📈 Analizar", scale=1)

    # Este Markdown mostrará el resultado sin borde, sin caja
    resultado = gr.Textbox(label="📋 Informe generado", lines=12, interactive=False, show_copy_button=True)
    #imagen = gr.Image()
    galeria = gr.Gallery(label="📊 Gráficos del análisis", columns=2, rows=3, height=650)



    boton.click(fn=analizar_accion, inputs=ticker_input, outputs=[resultado, galeria])



app.launch()
