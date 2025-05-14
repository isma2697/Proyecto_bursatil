import cohere

# Configura tu API Key de Cohere
co = cohere.Client("Onrem7Z1OH8cqTF20mLfXDmBDQ3qH8xm4DurvFjN")  # tu clave actual

def analizar_sentimiento(ticker):
    try:
        noticias = [
            f"{ticker} lanza nuevos productos innovadores.",
            f"Preocupación por la caída en ventas de {ticker}.",
            f"{ticker} anuncia expansión internacional."
        ]

        contenido = "\n".join([f"- {n}" for n in noticias])

        prompt = (
            f"Analiza el sentimiento general (positivo, negativo o neutral) "
            f"de las siguientes noticias sobre la empresa {ticker}:\n\n{contenido}\n\n"
            f"Responde solo con una palabra: Positivo, Negativo o Neutral."
        )

        # ✅ Cohere V1 usa 'message', no 'messages'
        respuesta = co.chat(
            model="command-nightly",  # modelo gratuito válido
            message=prompt
        )

        sentimiento = respuesta.text.strip()
        return f"Sentimiento general detectado: {sentimiento}"

    except Exception as e:
        return f"Error al analizar sentimiento: {str(e)}"
