# appRecetas/admin.py
from django.contrib import admin
from .models import Categoria, Receta, Ingrediente, Favorito

# Registra cada modelo
admin.site.register(Categoria)
admin.site.register(Receta)
admin.site.register(Ingrediente)
admin.site.register(Favorito)
