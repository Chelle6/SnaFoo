from django.contrib import admin

from .models import snack

class SnackAdmin(admin.ModelAdmin):
	list_display = ['name', 'optional']

admin.site.register(snack, SnackAdmin)