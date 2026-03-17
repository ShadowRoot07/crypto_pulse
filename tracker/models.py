from django.db import models
from django.contrib.auth.models import User

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, unique=True) # ej: BTC, ETH
    coingecko_id = models.CharField(max_length=50, unique=True) # Para la API
    current_price = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    image_url = models.URLField(blank=True, null=True)
    price_change_24h = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name_plural = "Cryptocurrencies"

class PriceHistory(models.Model):
    """Modelo para almacenar el historial y generar las gráficas"""
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='history')
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class ChatMessage(models.Model):
    BOT_TYPES = [
        ('USER', 'Usuario'),
        ('NEWS', 'Shadow News Bot'),
        ('TECH', 'Advisor Bot (IA)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sender_type = models.CharField(max_length=10, choices=BOT_TYPES, default='USER')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_type}: {self.message[:30]}"

