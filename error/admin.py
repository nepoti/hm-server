from django.contrib import admin
from models import Error


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ('message', 'timestamp')
