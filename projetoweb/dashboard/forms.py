from django import forms
from dashboard.models import Favoritos

class FavoritosForm(forms.ModelForm):
    class Meta:
        model = Favoritos
        fields = ['nome']
