import os
from groq import Groq
from .models import Cryptocurrency

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_ai_prediction(crypto_symbol, amount):
    """Analiza la compra/venta de una cantidad específica"""
    try:
        crypto = Cryptocurrency.objects.get(symbol=crypto_symbol.upper())
        trend = "alcista" if crypto.price_change_24h > 0 else "bajista"
        
        prompt = f"""
        Actúa como un analista técnico experto en criptomonedas con estilo Cyberpunk.
        El usuario quiere operar {amount} {crypto.symbol}.
        Datos actuales:
        - Precio: ${crypto.current_price}
        - Cambio 24h: {crypto.price_change_24h}% (Tendencia {trend})
        
        Da un veredicto breve de COMPRA, VENTA o HOLD, justificando técnicamente pero con actitud.
        Mantén la respuesta en menos de 100 palabras.
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec", # O el modelo que prefieras de Groq
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error en la Matrix: {str(e)}"

