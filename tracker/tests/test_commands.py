from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from tracker.models import Cryptocurrency

class TestCommands(TestCase):
    def setUp(self):
        # Creamos una crypto base para que el bot tenga donde asociar noticias
        Cryptocurrency.objects.create(
            name="Bitcoin", symbol="BTC", current_price=50000, price_change_24h=2
        )

    @patch('requests.get')
    @patch('tracker.ai_logic.ask_oracle')
    def test_run_news_bot_success(self, mock_oracle, mock_requests):
        """Simula el flujo completo del bot de noticias"""
        # 1. Simulamos el HTML de una web de noticias
        mock_html = MagicMock()
        mock_html.status_code = 200
        mock_html.text = '<html><div class="news-item">Bitcoin sube a la luna hoy</div></html>'
        mock_requests.return_value = mock_html

        # 2. Simulamos que la IA procesa la noticia correctamente
        mock_oracle.return_value = "RESUMEN CYBERPUNK: El mercado está en llamas por BTC."

        # 3. Llamamos al comando (ajusta el nombre si el tuyo es diferente)
        call_command('run_news_bot')

        # Verificamos que se intentó hacer el scraping
        self.assertTrue(mock_requests.called)
        # Verificamos que se llamó a la IA para resumir
        self.assertTrue(mock_oracle.called)

