import factory
from tracker.models import Cryptocurrency, ChatMessage
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')

class CryptoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cryptocurrency
    name = factory.Faker('company')
    symbol = factory.Faker('lexify', text='???', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    current_price = factory.Faker('pyfloat', left_digits=5, right_digits=2, positive=True)
    price_change_24h = factory.Faker('pyfloat', left_digits=1, right_digits=2)

class ChatMessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatMessage
    user = factory.SubFactory(UserFactory)
    message = factory.Faker('sentence')
    sender_type = 'USER'

