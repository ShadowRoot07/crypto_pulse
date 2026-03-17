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
        # 1. Simulamos una respuesta de red exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        # IMPORTANTE: Asegúrate de que el HTML tenga lo que el bot busca.
        # Si tu bot busca 'h2', este HTML funcionará:
        mock_response.text = """
        <html>
            <body>
                <article>
                    <h2>Bitcoin rompe records de nuevo</h2>
                </article>
            </body>
        </html>
        """
        mock_requests.return_value = mock_response

        # 2. Simulamos que la IA responde algo
        mock_oracle.return_value = "IA: Noticia procesada"

        # 3. Ejecutamos el comando
        call_command('run_news_bot')

        # 4. Verificamos
        self.assertTrue(mock_oracle.called, "La IA debería haber sido llamada")

