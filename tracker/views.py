from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cryptocurrency, ChatMessage
# Importamos las funciones inteligentes que creamos
from .ai_logic import get_ai_prediction, ask_oracle, client 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def dashboard(request):
    cryptos = Cryptocurrency.objects.all().order_by('-current_price')
    selected_symbol = request.GET.get('symbol', 'BTC')
    selected_crypto = cryptos.filter(symbol=selected_symbol).first()

    if not selected_crypto:
        selected_crypto = cryptos.first()

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
    """Maneja el chat con respuesta automática de IA rotativa"""
    if request.method == 'POST':
        user_msg = request.POST.get('message')
        if user_msg:
            ChatMessage.objects.create(user=request.user, message=user_msg, sender_type='USER')

            # Usamos ask_oracle para aprovechar el filtro de modelos automáticos
            ai_reply = ask_oracle(
                prompt=f"El usuario dice: {user_msg}",
                system_prompt="Eres el núcleo de IA de ShadowPulse. Respuestas breves, técnicas y con estilo hacker."
            )
            
            ChatMessage.objects.create(user=request.user, message=ai_reply, sender_type='BOT')

        return redirect('chat_bot')

    messages = ChatMessage.objects.all().order_by('-timestamp')[:50]
    return render(request, 'tracker/chat.html', {'messages': messages})

@login_required
def wiki_view(request):
    """El Oráculo de conocimiento Blockchain con Failover"""
    ai_response = None
    if request.method == 'POST':
        user_query = request.POST.get('query') or request.POST.get('message')

        if user_query:
            # Usamos la función inteligente de ai_logic
            ai_response = ask_oracle(
                prompt=user_query,
                system_prompt="Eres un tutor de criptomonedas en un futuro distópico. Responde con estilo Cyberpunk."
            )
        else:
            ai_response = "No se recibió ninguna consulta. Intente de nuevo."

    return render(request, 'tracker/wiki.html', {'ai_response': ai_response})

@csrf_exempt
@login_required
def predict_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            symbol = data.get('symbol')
            amount = data.get('amount')
            # Esta función ya tiene el filtro de modelos incorporado en ai_logic
            prediction = get_ai_prediction(symbol, amount)
            return JsonResponse({'prediction': prediction})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

