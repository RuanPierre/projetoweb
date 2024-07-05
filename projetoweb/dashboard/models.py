from django.db import models
from users.models import User

class Localizacao(models.Model):
    rua = models.CharField(max_length=150)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length= 50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.rua

class DadosEnergia(models.Model):
    producao_fotovoltaica = models.FloatField()
    irradiacao_direta_normal = models.FloatField()
    irradiacao_global_horizontal = models.FloatField()
    irradiacao_global_inclinada = models.FloatField()


    def __str__(self):
        return str(self.producao_fotovoltaica)

class Favoritos(models.Model):
    nome = models.CharField(max_length=150)
    dados_energia = models.ForeignKey(DadosEnergia, on_delete=models.CASCADE)
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
