from django import forms
from .models import Receta, Ingrediente, Favorito 
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['titulo', 'descripcion', 'pasos', 'tiempo_preparacion', 'tiempo_coccion', 'porciones', 'instrucciones', 'dificultad', 'id_categoria']

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'cantidad', 'receta'] 