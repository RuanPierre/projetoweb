from django.test import TestCase
from django.contrib.auth import get_user_model
from dashboard.models import Localizacao, DadosEnergia, Favoritos

User = get_user_model()

class LocalizacaoModelTest(TestCase):

    def setUp(self):
        self.localizacao = Localizacao.objects.create(
            rua='Centro',
            cidade='Caxias do Sul',
            estado='Rio Grande do Sul',
            latitude= -29.165783,
            longitude= -51.168021
        )

    def test_localizacao_creation(self):
        self.assertEqual(self.localizacao.rua, 'Centro')
        self.assertEqual(self.localizacao.cidade, 'Caxias do Sul')
        self.assertEqual(self.localizacao.estado, 'Rio Grande do Sul')
        self.assertEqual(self.localizacao.latitude, -29.165783),
        self.assertEqual(self.localizacao.longitude, -51.168021)
        self.assertEqual(str(self.localizacao), 'Centro')


class DadosEnergiaModelTest(TestCase):

    def setUp(self):
        self.dados_energia = DadosEnergia.objects.create(
            producao_fotovoltaica=1000.0,
            irradiacao_direta_normal=1500.0,
            irradiacao_global_horizontal=1800.0,
            irradiacao_global_inclinada=1700.0
        )

    def test_dados_energia_creation(self):
        self.assertEqual(self.dados_energia.producao_fotovoltaica, 1000.0)
        self.assertEqual(self.dados_energia.irradiacao_direta_normal, 1500.0)
        self.assertEqual(self.dados_energia.irradiacao_global_horizontal, 1800.0)
        self.assertEqual(self.dados_energia.irradiacao_global_inclinada, 1700.0)
        self.assertEqual(str(self.dados_energia), '1000.0')


class FavoritosModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password=':k6/:Yjo42VE'
        )
        self.localizacao = Localizacao.objects.create(
            rua='Centro',
            cidade='Caxias do Sul',
            estado='Rio Grande do Sul',
            latitude= -29.165783,
            longitude= -51.168021
        )
        self.dados_energia = DadosEnergia.objects.create(
            producao_fotovoltaica=1000.0,
            irradiacao_direta_normal=1500.0,
            irradiacao_global_horizontal=1800.0,
            irradiacao_global_inclinada=1700.0
        )
        self.favorito = Favoritos.objects.create(
            nome='Favorito Exemplo',
            dados_energia=self.dados_energia,
            localizacao=self.localizacao,
            user=self.user
        )

    def test_favoritos_creation(self):
        self.assertEqual(self.favorito.nome, 'Favorito Exemplo')
        self.assertEqual(self.favorito.dados_energia, self.dados_energia)
        self.assertEqual(self.favorito.localizacao, self.localizacao)
        self.assertEqual(self.favorito.user, self.user)
        self.assertEqual(str(self.favorito), 'Favorito Exemplo')