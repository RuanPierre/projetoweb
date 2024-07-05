from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('favoritos/', views.favoritos, name="favoritos"),
    path('dados_fotovoltaicos/', views.dados_fotovoltaicos, name='fotovoltaicos'),
    path('create/', views.create, name='create'),
    path('edit/<int:pk>', views.edit, name='edit')
]

handler404 = 'dashboard.views.erro_404'
handler500 = 'dashboard.views.erro_500'