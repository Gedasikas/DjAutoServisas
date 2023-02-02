from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

class Automobilio_modelis(models.Model):
    marke = models.CharField(_('Manufacturer'), max_length=100, help_text='Įveskite automobilio markę (pvz.: Toyota')
    modelis = models.CharField(_('Model'), max_length=100, help_text='Įveskite automobilio modelį (pvz.: Corolla')

    def __str__(self):
        return (f"{self.marke} - {self.modelis}")

    class Meta:
        verbose_name = _('Vehicle\'s model')
        verbose_name_plural = _('Vehicle models')

class Automobilis(models.Model):
    valstybinis_nr = models.CharField(_('License plate number'), max_length=20)
    automobilio_modelis_id = models.ForeignKey('Automobilio_modelis', on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField(_('VIN code'), max_length=17)
    kliento_v = models.CharField(_('Name'), max_length=50)
    kliento_p = models.CharField(_('Surname'), max_length=50)
    paveikslelis = models.ImageField(_('Vehicle photo'), upload_to='paveiksleliai', null=True, blank=True)
    komentarai = HTMLField(_('Comments'), null=True, blank=True, default=_('No comments'))

    def __str__(self):
        return (f"{self.automobilio_modelis_id} ({self.valstybinis_nr})")

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

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

class Profilis(models.Model):
    vartotojas = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.vartotojas.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'
