import openai
import os

# Asegúrate de tener tu API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # o ponla directamente, aunque mejor por seguridad usar variables de entorno

def analizar_sentimiento(ticker):
    try:
        # Simulamos un pequeño conjunto de noticias de prueba
        noticias = [
            f"{ticker} lanza nuevos productos innovadores.",
            f"Preocupación por la caída en ventas de {ticker}.",
            f"{ticker} anuncia expansión internacional."
        ]

        # Creamos un resumen para enviar al modelo
        contenido = "\n".join([f"- {n}" for n in noticias])

        prompt = (
            f"Analiza el sentimiento general (positivo, negativo o neutral) "
            f"de las siguientes noticias sobre la empresa {ticker}:\n\n{contenido}\n\n"
            f"Devuelve solo una palabra: Positivo, Negativo o Neutral."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0  # Para que no invente
        )

        sentimiento = response.choices[0].message.content.strip()
        return f"Sentimiento general detectado: {sentimiento}"

    except Exception as e:
        return f"Error al analizar sentimiento: {str(e)}"
