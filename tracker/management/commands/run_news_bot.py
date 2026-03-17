from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from tracker.ai_logic import ask_oracle # Usamos nuestra lógica centralizada
from tracker.models import ChatMessage
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

            # Buscamos el titular (Ajustado para ser más flexible en tests)
            post = soup.find('div', class_='list-post') or soup.find('article')
            
            if not post or not post.find('h2'):
                self.stdout.write(self.style.ERROR("No se encontraron titulares."))
                return

            headline = post.find('h2').text.strip()

            # IA para resumir usando nuestro Oráculo (con failover)
            news_summary = ask_oracle(
                prompt=f"Resume esta noticia de cripto en una sola frase potente y estilo cyberpunk: {headline}",
                system_prompt="Eres un analista de noticias en un futuro distópico."
            )

            # Publicar como BOT
            admin = User.objects.filter(is_superuser=True).first() or User.objects.first()
            if admin:
                ChatMessage.objects.create(
                    user=admin,
                    message=f"📡 [DECODED_NEWS]: {news_summary}",
                    sender_type='BOT'
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Noticia publicada: {headline[:30]}..."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error en el enlace: {e}"))

