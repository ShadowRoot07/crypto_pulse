from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from tracker.models import Cryptocurrency, ChatMessage
from django.contrib.auth.models import User

class TestCommands(TestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", email="a@a.com", password="123")
        Cryptocurrency.objects.create(name="Bitcoin", symbol="BTC", current_price=50000, price_change_24h=2)

    @patch('requests.get')
    @patch('tracker.management.commands.run_news_bot.ask_oracle') # Apuntamos al path correcto
    def test_run_news_bot_success(self, mock_oracle, mock_requests):
        # 1. Simular HTML que coincida con el comando
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<div class="list-post"><h2>Bitcoin rompe records</h2></div>'
        mock_requests.return_value = mock_response

        # 2. Simular respuesta de la IA
        mock_oracle.return_value = "IA: Noticia procesada"

        # 3. Ejecutar
        call_command('run_news_bot')

        # 4. Verificar que se guardó el mensaje en la BD
        self.assertTrue(ChatMessage.objects.filter(message__contains="IA: Noticia procesada").exists())
        self.assertTrue(mock_oracle.called)

