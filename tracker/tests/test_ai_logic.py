from django.test import TestCase
from unittest.mock import patch, MagicMock
from tracker.ai_logic import ask_oracle, get_ai_prediction

class TestAILogic(TestCase):

    @patch('tracker.ai_logic.client.chat.completions.create')
    def test_ask_oracle_success(self, mock_groq):
        """Simula una respuesta exitosa de Groq"""
        # Configuramos el Mock para que devuelva lo que queremos
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Respuesta Cyberpunk Simulada"
        mock_groq.return_value = mock_response

        response = ask_oracle("¿Qué es un hash?")
        self.assertEqual(response, "Respuesta Cyberpunk Simulada")
        # Verificamos que se llamó a la API al menos una vez
        self.assertTrue(mock_groq.called)

    @patch('tracker.ai_logic.client.chat.completions.create')
    def test_ai_failover_logic(self, mock_groq):
        """Simula que el primer modelo falla y el segundo responde"""
        # El primer intento lanza un error, el segundo funciona
        mock_groq.side_effect = [Exception("Modelo caido"), MagicMock(choices=[MagicMock(message=MagicMock(content="Respuesta de respaldo"))])]
        
        response = ask_oracle("Test failover")
        self.assertEqual(response, "Respuesta de respaldo")

