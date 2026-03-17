from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chat/', views.chat_bot, name='chat_bot'),
    path('wiki/', views.wiki_view, name='wiki_view'),
    path('api/predict/', views.predict_api, name='predict_api'),
]

