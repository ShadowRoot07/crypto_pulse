from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cryptocurrency, ChatMessage
from .ai_logic import get_ai_prediction
from django.http import JsonResponse
import json

@login_required
def dashboard(request):
    cryptos = Cryptocurrency.objects.all().order_by('-current_price')
    
    # Obtener símbolo de la URL o usar BTC por defecto
    selected_symbol = request.GET.get('symbol', 'BTC')
    selected_crypto = cryptos.filter(symbol=selected_symbol).first()
    
    if not selected_crypto:
        selected_crypto = cryptos.first()

    # Obtener historial para la gráfica (últimas 20 entradas)
    history = selected_crypto.history.all().order_by('-timestamp')[:20][::-1]
    
    chart_labels = [h.timestamp.strftime('%H:%M') for h in history]
    chart_data = [float(h.price) for h in history]

    context = {
        'cryptos': cryptos,
        'selected_crypto': selected_crypto,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'title': 'Terminal de Mando'
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def chat_bot(request):
    """Maneja el chat interactivo"""
    if request.method == 'POST':
        user_msg = request.POST.get('message')
        ChatMessage.objects.create(user=request.user, message=user_msg, sender_type='USER')
        return redirect('chat_bot')

    messages = ChatMessage.objects.all().order_by('-timestamp')[:50]
    return render(request, 'tracker/chat.html', {'messages': messages})


@login_required
def wiki_view(request):
    ai_response = None
    if request.method == 'POST':
        user_query = request.POST.get('query')
        # Usamos Groq con un System Prompt de tutor educativo
        from .ai_logic import client
        
        prompt = f"Eres un instructor experto en Blockchain y Cripto. Responde de forma clara y con estilo Cyberpunk a: {user_query}"
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-specdec",
                messages=[{"role": "system", "content": "Eres un tutor de criptomonedas en un futuro distópico."},
                          {"role": "user", "content": prompt}],
            )
            ai_response = completion.choices[0].message.content
        except:
            ai_response = "Error al conectar con la base de datos de conocimiento..."

    return render(request, 'tracker/wiki.html', {'ai_response': ai_response})

