from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'categorias' 
    def __str__(self):
        return self.nombre

class Receta(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)  
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas_creadas', null=True, blank=True) 
    descripcion = models.TextField(blank=True, null=True)
    tiempo_preparacion = models.IntegerField(blank=True, null=True, help_text="En minutos") 
    tiempo_coccion = models.IntegerField(help_text="En minutos", blank=True, null=True)
    porciones = models.IntegerField(blank=True, null=True)
    instrucciones = models.TextField(blank=True, null=True) 
    pasos = models.TextField(blank=True, null=True) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    dificultad = models.CharField(
        max_length=10,
        choices=[('Fácil', 'Fácil'), ('Media', 'Media'), ('Difícil', 'Difícil')],
        default='Media'
    )
    id_categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, db_column='id_categoria')

    class Meta:
        db_table = 'recetas' 

    def __str__(self):
        return self.titulo

class Ingrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=50, default="cantidad a definir")
    
    def __str__(self):
        return f"{self.cantidad} de {self.nombre} ({self.receta.nombre})"

    class Meta:
        unique_together = ('receta', 'nombre')

class Favorito(models.Model):  
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, null=True, blank=True)
    fecha_guardado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favoritos'
        unique_together = ('usuario', 'receta') 
        verbose_name = "Receta Favorita"
        verbose_name_plural = "Recetas Favoritas"

    def __str__(self):
        return f"{self.usuario.username} ♥ {self.receta.titulo}" 