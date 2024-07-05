from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from dashboard.forms import FavoritosForm
from .models import DadosEnergia, Localizacao, Favoritos
import rasterio
import os


def home(request):
    return render(request, 'home.html')

@login_required
def favoritos(request):
    dados = {}
    form = FavoritosForm()
    dados['fav'] = Favoritos.objects.filter(user=request.user).prefetch_related('dados_energia', 'localizacao')
    return render(request, 'favoritos.html', dados)

def form(request):
    data = {}
    data['form'] = FavoritosForm
    return render (request, 'form.html', data)

@login_required
def create(request):
    if request.method == 'POST':
        form = FavoritosForm(request.POST or None)
        if form.is_valid():
            favorito = form.save(commit=False)
            favorito.user = request.user

            dados_energia_data = request.POST.get('dados_energia')
            localizacao_data = request.POST.get('localizacao')
            dados_energia_dict = json.loads(dados_energia_data)
            localizacao_dict = json.loads(localizacao_data)

            dados_energia, created = DadosEnergia.objects.get_or_create(**dados_energia_dict)
            favorito.dados_energia = dados_energia

            localizacao, created = Localizacao.objects.get_or_create(**localizacao_dict)
            favorito.localizacao = localizacao

            favorito.save()
            messages.success(request,f'Favorito adicionado com sucesso')
            return redirect('favoritos')
    else:
        form = FavoritosForm()
    return render(request, 'home.html', {'form': form})

def delete(request, pk):
    fav = Favoritos.objects.get(pk=pk)
    fav.delete()
    return redirect('favoritos')

def dados_fotovoltaicos(request):
    try:
        latitude = float(request.GET.get('latitude'))
        longitude = float(request.GET.get('longitude'))

        # Caminho absoluto dos arquivos
        pvout_file_path = os.path.join(os.path.dirname(__file__), 'static', 'dados_energia', 'PVOUT.tif')
        dni_file_path = os.path.join(os.path.dirname(__file__), 'static', 'dados_energia', 'DNI.tif')
        ghi_file_path = os.path.join(os.path.dirname(__file__), 'static', 'dados_energia', 'GHI.tif')
        gti_file_path = os.path.join(os.path.dirname(__file__), 'static', 'dados_energia', 'GTI.tif')

        dados_tif = {}

        with rasterio.open(pvout_file_path) as src_pvout:
            row_pvout, col_pvout = src_pvout.index(longitude, latitude)
            solar_data_pvout = float(src_pvout.read(1)[row_pvout, col_pvout])
            dados_tif['solar_data_pvout'] = solar_data_pvout


        with rasterio.open(dni_file_path) as src_dni:
            row_dni, col_dni = src_dni.index(longitude, latitude)
            solar_data_dni = float(src_dni.read(1)[row_dni, col_dni])
            dados_tif['solar_data_dni'] = solar_data_dni

        with rasterio.open(ghi_file_path) as src_ghi:
            row_ghi, col_ghi = src_ghi.index(longitude, latitude)
            solar_data_ghi = float(src_ghi.read(1)[row_ghi, col_ghi])
            dados_tif['solar_data_ghi'] = solar_data_ghi

        with rasterio.open(gti_file_path) as src_gti:
            row_gti, col_gti = src_gti.index(longitude, latitude)
            solar_data_gti = float(src_gti.read(1)[row_gti, col_gti])
            dados_tif['solar_data_gti'] = solar_data_gti

        # Retorna os dados de produção fotovoltaica
        return JsonResponse(dados_tif)

    except Exception as e:
        # Log do erro
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

def erro_404(request, exception):
    return render(request, '404.html', status=404)

def erro_500(request):
    return render(request, '500.html', status=500)

