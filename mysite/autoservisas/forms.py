from .models import UzsakymoKomentarai
from .models import Profilis
from django import forms
from django.contrib.auth.models import User

class UzsakymoKomentaraiForma(forms.ModelForm):
    class Meta:
        model = UzsakymoKomentarai
        fields = ('komentaras', 'uzsakymas', 'komentatorius',)
        widgets = {'uzsakymas': forms.HiddenInput(), 'komentatorius': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']
class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']