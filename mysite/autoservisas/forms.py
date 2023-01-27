from .models import UzsakymoKomentarai
from django import forms

class UzsakymoKomentaraiForma(forms.ModelForm):
    class Meta:
        model = UzsakymoKomentarai
        fields = ('komentaras', 'uzsakymas', 'komentatorius',)
        widgets = {'uzsakymas': forms.HiddenInput(), 'komentatorius': forms.HiddenInput()}