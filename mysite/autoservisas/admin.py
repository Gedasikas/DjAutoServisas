from django.contrib import admin

from .models import Automobilio_modelis, Automobilis, Uzsakymas, Uzsakymo_eilute, Paslauga, UzsakymoKomentarai

class Automobilio_modelisAdmin(admin.ModelAdmin):
    list_display = ('marke', 'modelis')

class Uzsakymo_eiluteInline(admin.TabularInline):
    model = Uzsakymo_eilute
    extra = 0

class UzsakymasAdmin(admin.ModelAdmin):
     list_display = ('automobilis_id', 'data', 'bendra_suma', 'status')
     inlines = [Uzsakymo_eiluteInline]

class Uzsakymo_eiluteAdmin(admin.ModelAdmin):
    list_display = ('paslauga_id', 'uzsakymas_id', 'kiekis', 'suma', 'status')

class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('automobilio_modelis_id', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('kliento_p', 'automobilio_modelis_id')
    search_fields = ('vin_kodas', 'valstybinis_nr')

class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')

class UzsakymoKomentaraiAdmin(admin.ModelAdmin):
    list_display = ('uzsakymas', 'komentatorius', 'komentaro_data', 'komentaras' )



admin.site.register(Automobilio_modelis, Automobilio_modelisAdmin)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Uzsakymo_eilute, Uzsakymo_eiluteAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(UzsakymoKomentarai, UzsakymoKomentaraiAdmin)