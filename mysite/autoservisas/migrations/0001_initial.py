# Generated by Django 4.1.5 on 2023-01-27 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Automobilio_modelis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marke', models.CharField(help_text='Įveskite automobilio markę (pvz.: Toyota', max_length=100, verbose_name='Markė')),
                ('modelis', models.CharField(help_text='Įveskite automobilio modelį (pvz.: Corolla', max_length=100, verbose_name='Modelis')),
            ],
            options={
                'verbose_name': 'Automobilio modelis',
                'verbose_name_plural': 'Automobilių modeliai',
            },
        ),
        migrations.CreateModel(
            name='Automobilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valstybinis_nr', models.CharField(max_length=20, verbose_name='Valstybinis_NR')),
                ('vin_kodas', models.CharField(max_length=17, verbose_name='VIN_Kodas')),
                ('kliento_v', models.CharField(max_length=50, verbose_name='Vardas')),
                ('kliento_p', models.CharField(max_length=50, verbose_name='Pavardė')),
                ('paveikslelis', models.ImageField(blank=True, null=True, upload_to='paveiksleliai', verbose_name='Mašinos paveikslėlis')),
                ('komentarai', tinymce.models.HTMLField(blank=True, default='Nėra komentarų', null=True, verbose_name='Komentarai')),
                ('automobilio_modelis_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.automobilio_modelis')),
            ],
            options={
                'verbose_name': 'Automobilis',
                'verbose_name_plural': 'Automobiliai',
            },
        ),
        migrations.CreateModel(
            name='Paslauga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(max_length=100, verbose_name='Pavadinimas')),
                ('kaina', models.FloatField(verbose_name='Kaina')),
                ('aprasymas', models.TextField(default='Aprašymo nėra', help_text='Trumpas paslaugos aprašymas', max_length=2000, null=True, verbose_name='Aprašymas')),
            ],
            options={
                'verbose_name': 'Paslauga',
                'verbose_name_plural': 'Paslaugos',
            },
        ),
        migrations.CreateModel(
            name='Uzsakymas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Užsakymo data')),
                ('ivykdytas_iki', models.DateField(blank=True, null=True, verbose_name='Užsakymas bus įvykdytas iki')),
                ('status', models.CharField(blank=True, choices=[('t', 'Tvarkoma'), ('a', 'Atsiimta'), ('g', 'Galima atsiimti')], default='t', help_text='Statusas', max_length=1)),
                ('automobilis_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autoservisas.automobilis')),
                ('uzsakovas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Užsakymas',
                'verbose_name_plural': 'Užsakymai',
            },
        ),
        migrations.CreateModel(
            name='UzsakymoKomentarai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('komentaro_data', models.DateTimeField(auto_now_add=True)),
                ('komentaras', models.TextField(max_length=2000, verbose_name='Komentaras')),
                ('komentatorius', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('uzsakymas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uzsakymo_komentarai', to='autoservisas.uzsakymas')),
            ],
            options={
                'verbose_name': 'Komentaras',
                'verbose_name_plural': 'Komentarai',
                'ordering': ['-komentaro_data'],
            },
        ),
        migrations.CreateModel(
            name='Uzsakymo_eilute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiekis', models.IntegerField(null=True, verbose_name='Kiekis')),
                ('status', models.CharField(blank=True, choices=[('t', 'Tvarkoma'), ('a', 'Atšaukta'), ('p', 'Papildomi gedimai'), ('s', 'Sutvarkyta')], default='t', help_text='Statusas', max_length=1)),
                ('paslauga_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.paslauga')),
                ('uzsakymas_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eilutes', to='autoservisas.uzsakymas')),
            ],
            options={
                'verbose_name': 'Užsakymo eilė',
                'verbose_name_plural': 'Užsakymų eilutės',
            },
        ),
    ]
