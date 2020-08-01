from django.contrib import admin
from wenku.models import Wenku
# Register your models here.
@admin.register(Wenku)
class WenkuAdmin(admin.ModelAdmin):
    list_display = ['title']











