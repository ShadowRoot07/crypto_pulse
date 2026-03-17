from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from tracker.ai_logic import client
from tracker.models import ChatMessage, Cryptocurrency
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Scrapea noticias reales y las publica en el chat con estilo Cyberpunk'

    def handle(self, *args, **options):
        self.stdout.write("🌐 Escaneando satélites en busca de noticias...")
        url = "https://cryptoslate.com/news/"
        headers = {'User-Agent': 'Mozilla/5.0'}

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos el primer titular (ajustado a la estructura de CryptoSlate)
            post = soup.find('div', class_='list-post')
            if not post:
                self.stdout.write(self.style.ERROR("No se encontraron titulares."))
                return

            headline = post.find('h2').text.strip()
            
            # IA para resumir
            prompt = f"Resume esta noticia de cripto en una sola frase potente y estilo cyberpunk para un chat de hackers: {headline}"
            completion = client.chat.completions.create(
                model="llama-3.3-70b-specdec",
                messages=[{"role": "user", "content": prompt}]
            )
            news_summary = completion.choices[0].message.content

            # Publicar como BOT
            admin = User.objects.filter(is_superuser=True).first()
            ChatMessage.objects.create(
                user=admin, 
                message=f"📡 [DECODED_NEWS]: {news_summary}", 
                sender_type='BOT'
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Noticia publicada: {headline[:30]}..."))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error en el enlace: {e}"))

