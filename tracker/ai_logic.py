import os
from groq import Groq
from .models import Cryptocurrency

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Lista de modelos gratuitos ordenados por "calidad"
# Si uno falla o es retirado, el sistema salta al siguiente automáticamente.
AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",  # El más potente actual
    "llama-3-70b-8192",         # Clásico confiable
    "llama-3-8b-8192",          # Ultra rápido
    "mixtral-8x7b-32768",       # Muy bueno para análisis
    "gemma2-9b-it"              # Opción ligera de Google
]

def get_ai_prediction(crypto_symbol, amount):
    """Analiza la compra/venta usando el mejor modelo disponible"""
    try:
        crypto = Cryptocurrency.objects.get(symbol=crypto_symbol.upper())
        trend = "alcista" if crypto.price_change_24h > 0 else "bajista"

        prompt = f"""
        Actúa como un analista técnico experto en criptomonedas con estilo Cyberpunk.
        El usuario quiere operar {amount} {crypto.symbol}.
        Datos actuales:
        - Precio: ${crypto.current_price}
        - Cambio 24h: {crypto.price_change_24h}% (Tendencia {trend})

        Da un veredicto breve de COMPRA, VENTA o HOLD, justificando técnicamente con actitud hacker.
        Respuesta en menos de 80 palabras.
        """

        # --- FILTRO AUTOMÁTICO DE MODELOS ---
        for model_name in AVAILABLE_MODELS:
            try:
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=10.0 # No queremos esperar una eternidad si el modelo está caído
                )
                # Si llegamos aquí, el modelo funcionó. Devolvemos la respuesta.
                return completion.choices[0].message.content
            except Exception as e:
                # Si este modelo falla, imprimimos el error en consola y pasamos al siguiente
                print(f"DEBUG: Modelo {model_name} falló. Intentando siguiente... Error: {e}")
                continue

        return "Error: Ningún núcleo de IA respondió. El sistema está offline."

    except Exception as e:
        return f"Error en la Matrix: {str(e)}"


def ask_oracle(prompt, system_prompt="Eres un tutor de criptomonedas."):
    """Función genérica para el Oráculo que también rota modelos"""
    for model_name in AVAILABLE_MODELS:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                timeout=10.0
            )
            return completion.choices[0].message.content
        except Exception:
            continue
    return "Error al conectar con la base de datos de conocimiento..."

