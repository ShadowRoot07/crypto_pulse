import requests
from .models import Cryptocurrency, PriceHistory

def update_crypto_data():
    """Trae el Top 10 de criptomonedas y actualiza la DB"""
    # Los 10 IDs más relevantes según CoinGecko
    crypto_ids = "bitcoin,ethereum,binancecoin,solana,ripple,cardano,dogecoin,polkadot,tron,chainlink"
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'ids': crypto_ids,
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()

        for item in data:
            crypto, created = Cryptocurrency.objects.update_or_create(
                coingecko_id=item['id'],
                defaults={
                    'name': item['name'],
                    'symbol': item['symbol'].upper(),
                    'current_price': item['current_price'],
                    'image_url': item['image'],
                    'price_change_24h': item['price_change_percentage_24h'],
                }
            )
            # Guardamos un punto en el historial para la gráfica
            PriceHistory.objects.create(crypto=crypto, price=item['current_price'])
            
        return True
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")
        return False

