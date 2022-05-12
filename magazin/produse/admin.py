from django.contrib import admin

# Register your models here.
from produse.models import Produse, Poze
from produse.models import Comanda, Useri

class PozeAdminInline(admin.TabularInline):
    model = Poze


class ProduseAdmin(admin.ModelAdmin):
    inlines = (PozeAdminInline,)
    list_display = ["nume", "marca", "pret", "stoc"]


admin.site.register(Produse,ProduseAdmin)


class ComandaAdminInline(admin.TabularInline):
    model = Comanda


class UseriAdmin(admin.ModelAdmin):
    inlines = (ComandaAdminInline,)
    list_display = ["user", "adresa", "telefon"]


admin.site.register(Useri, UseriAdmin)
