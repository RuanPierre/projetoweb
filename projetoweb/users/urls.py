from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.entrar, name='login'),
    path('logout/', views.sair, name='sair'),
    path('cadastro/', views.cadastro, name='cadastro'),
    ]