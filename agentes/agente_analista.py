def generar_informe(datos_financieros, datos_sentimiento):
    try:
        # Analizar tendencia, volatilidad y sentimiento
        tendencia = "Alcista" if "Alcista" in datos_financieros else "Bajista"
        volatilidad = "Alta" if "Alta" in datos_financieros else ("Media" if "Media" in datos_financieros else "Baja")
        sentimiento = "Positivo" if "Positivo" in datos_sentimiento else ("Negativo" if "Negativo" in datos_sentimiento else "Neutral")

        # Lógica simple de recomendación
        if tendencia == "Alcista" and sentimiento == "Positivo" and volatilidad != "Alta":
            recomendacion = "Comprar"
        elif tendencia == "Bajista" and sentimiento == "Negativo":
            recomendacion = "Vender"
        else:
            recomendacion = "Mantener"

        # Crear informe bonito
        informe = (
            f"Análisis Financiero:\n{datos_financieros}\n\n"
            f"Análisis de Sentimiento:\n{datos_sentimiento}\n\n"
            f"Recomendación final: **{recomendacion}**\n\n"
            f"Motivo: Basado en la tendencia actual ({tendencia}), "
            f"nivel de volatilidad ({volatilidad}) y sentimiento de mercado ({sentimiento})."
        )

        return informe

    except Exception as e:
        return f"Error al generar informe: {str(e)}"
