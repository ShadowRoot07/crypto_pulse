from django.core.management.base import BaseCommand
from tracker.models import ChatMessage, Cryptocurrency, PriceHistory

class Command(BaseCommand):
    help = 'Limpia los registros del sistema (mensajes e historial)'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Borra absolutamente todo')

    def handle(self, *args, **options):
        if options['all']:
            ChatMessage.objects.all().delete()
            PriceHistory.objects.all().delete()
            # Cryptocurrency.objects.all().delete() # Opcional: Borrar también las monedas
            self.stdout.write(self.style.WARNING("☣️ BASE DE DATOS PURGADA POR COMPLETO."))
        else:
            ChatMessage.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("🧹 Historial de mensajes limpio."))

