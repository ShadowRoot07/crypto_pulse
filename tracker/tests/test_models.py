from django.test import TestCase
from .factories import CryptoFactory, ChatMessageFactory

class TestCryptoModels(TestCase):
    def test_crypto_creation_with_factory(self):
        crypto = CryptoFactory(name="Ethereum", symbol="ETH")
        self.assertEqual(str(crypto), "Ethereum (ETH)")

    def test_bulk_messages(self):
        # Crear 10 mensajes aleatorios en un segundo
        messages = ChatMessageFactory.create_batch(10)
        self.assertEqual(len(messages), 10)

