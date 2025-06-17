from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('crear/', views.crear_receta_y_ingredientes, name='crear_receta'),
    path('editar/<int:receta_id>/', views.editar_receta, name='editar_receta'),
    path('eliminar/<int:receta_id>/', views.eliminar_receta, name='eliminar_receta'),
    path('favoritos/', views.ver_favoritos, name='ver_favoritos'),
    path('favorito/<int:receta_id>/', views.agregar_favorito, name='agregar_favorito'),
    path('editar-ingrediente/<int:ingrediente_id>/', views.editar_ingrediente, name='editar_ingrediente'),
path('eliminar-ingrediente/<int:ingrediente_id>/', views.eliminar_ingrediente, name='eliminar_ingrediente'),
path('quitar-favorito/<int:receta_id>/', views.quitar_favorito, name='quitar_favorito'),


    

]
