import requests
from bs4 import BeautifulSoup
from .ai_logic import client
from .models import ChatMessage
from django.contrib.auth.models import User

def fetch_and_post_news():
    print("🌐 Escaneando la red en busca de noticias...")
    url = "https://cointelegraph.com/tags/bitcoin" # Ejemplo de fuente
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer el primer titular relevante (esto depende del HTML del sitio)
        headline = soup.find('span', class_='post-card-inline__title').text.strip()
        
        # Usar IA para resumir y darle estilo
        prompt = f"Resume esta noticia de cripto en una sola frase potente y estilo cyberpunk: {headline}"
        completion = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=[{"role": "user", "content": prompt}]
        )
        news_summary = completion.choices[0].message.content

        # Publicar en el chat como el BOT
        admin_user = User.objects.filter(is_superuser=True).first()
        ChatMessage.objects.create(
            user=admin_user, 
            message=f"📡 [NEWS_UPDATE]: {news_summary}", 
            sender_type='BOT'
        )
        print("✅ Noticia publicada en el chat.")
        
    except Exception as e:
        print(f"❌ Error en el escaneo: {e}")

