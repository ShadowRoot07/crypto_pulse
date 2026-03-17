from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tracker.models import Cryptocurrency

class TestTrackerViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        Cryptocurrency.objects.create(name="Ethereum", symbol="ETH", current_price=3000, price_change_24h=1)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/dashboard.html')

    def test_predict_api_mock(self):
        """Prueba la API de predicción simulando la respuesta de la IA"""
        with patch('tracker.views.get_ai_prediction') as mock_pred:
            mock_pred.return_value = "VERDICTO: HOLD"
            response = self.client.post(
                reverse('predict_api'),
                data='{"symbol": "ETH", "amount": 1}',
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("HOLD", response.json()['prediction'])

