from django.contrib import admin
from .models import Email

# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    readonly_fields = ('email', 'register', 'id')
    list_display = ('email', 'register')
    ordering = ('-register',)

admin.site.register(Email, EmailAdmin)
