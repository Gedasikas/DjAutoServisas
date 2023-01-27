from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField

class Automobilio_modelis(models.Model):
    marke = models.CharField('Markė', max_length=100, help_text='Įveskite automobilio markę (pvz.: Toyota')
    modelis = models.CharField('Modelis', max_length=100, help_text='Įveskite automobilio modelį (pvz.: Corolla')

    def __str__(self):
        return (f"{self.marke} - {self.modelis}")

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilių modeliai'

class Automobilis(models.Model):
    valstybinis_nr = models.CharField('Valstybinis_NR', max_length=20)
    automobilio_modelis_id = models.ForeignKey('Automobilio_modelis', on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField('VIN_Kodas', max_length=17)
    kliento_v = models.CharField('Vardas', max_length=50)
    kliento_p = models.CharField('Pavardė', max_length=50)
    paveikslelis = models.ImageField('Mašinos paveikslėlis', upload_to='paveiksleliai', null=True, blank=True)
    komentarai = HTMLField('Komentarai', null=True, blank=True, default='Nėra komentarų')

    def __str__(self):
        return (f"{self.automobilio_modelis_id} ({self.valstybinis_nr})")

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'

class Uzsakymas(models.Model):
    data = models.DateField('Užsakymo data', null=True, blank=True)
    automobilis_id = models.ForeignKey('Automobilis', on_delete=models.CASCADE)
    ivykdytas_iki = models.DateField('Užsakymas bus įvykdytas iki', blank=True, null=True)
    uzsakovas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        if self.ivykdytas_iki and date.today() > self.ivykdytas_iki:
            return True
        return False


    STATUS = (
        ('t', 'Tvarkoma'),
        ('a', 'Atsiimta'),
        ('g', 'Galima atsiimti'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='t',
        help_text='Statusas',
    )

    def bendra_suma(self):
        suma = 0
        eilutes = self.eilutes.all()
        for eilute in eilutes:
            suma += eilute.suma()
        return suma

    def __str__(self):
        return (f"{self.automobilis_id} {self.data}")

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'

class UzsakymoKomentarai(models.Model):
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True, related_name='uzsakymo_komentarai')
    komentatorius = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    komentaro_data = models.DateTimeField(auto_now_add=True)
    komentaras = models.TextField('Komentaras', max_length=2000)

    class Meta:
        verbose_name = "Komentaras"
        verbose_name_plural = 'Komentarai'
        ordering = ['-komentaro_data']

class Uzsakymo_eilute(models.Model):
    paslauga_id = models.ForeignKey('Paslauga', on_delete=models.SET_NULL, null=True)
    uzsakymas_id = models.ForeignKey('Uzsakymas', on_delete=models.CASCADE, related_name='eilutes')
    kiekis = models.IntegerField('Kiekis', null=True)

    STATUS = (
        ('t', 'Tvarkoma'),
        ('a', 'Atšaukta'),
        ('p', 'Papildomi gedimai'),
        ('s', 'Sutvarkyta'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='t',
        help_text='Statusas',
    )

    def suma(self):
        return self.paslauga_id.kaina * self.kiekis

    def __str__(self):
        return (f"{self.uzsakymas_id} {self.paslauga_id} {self.kiekis} {self.suma()}")

    class Meta:
        verbose_name = 'Užsakymo eilė'
        verbose_name_plural = 'Užsakymų eilutės'

class Paslauga(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100)
    kaina = models.FloatField('Kaina')
    aprasymas = models.TextField('Aprašymas', max_length=2000, help_text='Trumpas paslaugos aprašymas', default='Aprašymo nėra', null=True)

    def __str__(self):
        return (f"{self.pavadinimas}")

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'
