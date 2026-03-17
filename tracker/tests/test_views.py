from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tracker.models import Cryptocurrency
import json

class TestTrackerViews(TestCase):
    def setUp(self):
        self.client = Client()
        # Usamos un password simple
        self.password = "password123"
        self.user = User.objects.create_user(username="testuser", password=self.password)
        self.client.login(username="testuser", password=self.password)
        Cryptocurrency.objects.create(name="Ethereum", symbol="ETH", current_price=3000, price_change_24h=1)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    @patch('tracker.views.get_ai_prediction')
    def test_predict_api_mock(self, mock_pred): # Añadimos el mock_pred como argumento
        mock_pred.return_value = "VERDICTO: HOLD"
        response = self.client.post(
            reverse('predict_api'),
            data=json.dumps({"symbol": "ETH", "amount": 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("HOLD", response.json()['prediction'])

