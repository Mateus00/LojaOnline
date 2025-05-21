from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ("telefone", "endereco"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações adicionais", {
            "fields": ("telefone", "endereco"),
        }),
    )

    list_display = ("username", "email", "first_name", "last_name", "telefone", "is_staff")
    search_fields = ("username", "email", "telefone")
