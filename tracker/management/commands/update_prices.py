from django.core.management.base import BaseCommand
from tracker.utils import update_crypto_data

class Command(BaseCommand):
    help = 'Actualiza los precios del Top 10 de criptomonedas desde CoinGecko'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Conectando con CoinGecko...")
        success = update_crypto_data()
        if success:
            self.stdout.write(self.style.SUCCESS("✅ Precios actualizados con éxito."))
        else:
            self.stdout.write(self.style.ERROR("❌ Fallo al actualizar los precios."))

