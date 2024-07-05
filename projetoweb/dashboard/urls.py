from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('favoritos/', views.favoritos, name="favoritos"),
    path('dados_fotovoltaicos/', views.dados_fotovoltaicos, name='fotovoltaicos'),
    path('create/', views.create, name='create'),
    path('delete/<int:pk>', views.delete, name = 'delete')
]

handler404 = 'dashboard.views.erro_404'
handler500 = 'dashboard.views.erro_500'