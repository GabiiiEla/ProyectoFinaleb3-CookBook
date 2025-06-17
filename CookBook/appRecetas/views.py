from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecetaForm, IngredienteForm
from .models import Receta, Ingrediente, Favorito
from django.db.models import Q

@login_required
def crear_receta_y_ingredientes(request):
    receta_form = RecetaForm(request.POST or None)
    receta = None
    ingredientes = []

    if request.method == 'POST':

        if 'crear_receta' in request.POST and receta_form.is_valid():
            receta = receta_form.save(commit=False)

            receta.autor = request.user
            receta.save()
            messages.success(request, "Receta creada exitosamente. ¡Ahora agrega los ingredientes!")

            return render(request, 'crear_receta_y_ingredientes.html', {
                'receta_form': RecetaForm(instance=receta),
                'ingrediente_form': IngredienteForm(initial={'receta': receta}),
                'receta': receta,
                'ingredientes': receta.ingredientes.all()
            })

        elif 'agregar_ingrediente' in request.POST:

            receta_id = request.POST.get('receta_id')
            if not receta_id:
                messages.error(request, "Error: No se encontró la receta a la que añadir el ingrediente.")
                return redirect('crear_receta_y_ingredientes')

            receta = get_object_or_404(Receta, id=receta_id)

            if receta.autor != request.user:
                messages.error(request, "No tienes permiso para agregar ingredientes a esta receta.")
                return redirect('dashboard')
            ingrediente_form = IngredienteForm(request.POST)
            if ingrediente_form.is_valid():
                ingrediente = ingrediente_form.save(commit=False)
                ingrediente.receta = receta
                ingrediente.save()
                messages.success(request, "Ingrediente agregado exitosamente.")
            else:
                messages.error(request, "Error al agregar el ingrediente.")

            return render(request, 'crear_receta_y_ingredientes.html', {
                'receta_form': RecetaForm(instance=receta),
                'ingrediente_form': IngredienteForm(initial={'receta': receta}),
                'receta': receta,
                'ingredientes': receta.ingredientes.all()
            })
    return render(request, 'crear_receta_y_ingredientes.html', {
        'receta_form': receta_form,
        'ingrediente_form': IngredienteForm()
    })

@login_required
def dashboard(request):
    query = request.GET.get('q')

    recetas = Receta.objects.filter(autor=request.user).select_related('id_categoria')
    if query:
        recetas = recetas.filter(
            Q(ingredientes__nombre__icontains=query) |
            Q(titulo__icontains=query) 
        ).distinct()

    return render(request, 'dashboard.html', {
        'recetas': recetas,
        'query': query
    })

@login_required
def dashboard_usuario(request):
    return dashboard(request)

@login_required
def agregar_favorito(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    favorito, creado = Favorito.objects.get_or_create(usuario=request.user, receta=receta)

    if creado:
        messages.success(request, "Receta añadida a tus favoritos.")
    else:
        messages.info(request, "La receta ya estaba en tus favoritos.")

    return redirect('ver_favoritos')

@login_required
def ver_favoritos(request):

    favoritos = Favorito.objects.filter(usuario=request.user).select_related('receta')
    return render(request, 'favoritos.html', {'favoritos': favoritos})

@login_required
def editar_receta(request, receta_id):

    receta = get_object_or_404(Receta, id=receta_id, autor=request.user)

    if request.method == 'POST':
        if 'guardar_receta' in request.POST:
            form = RecetaForm(request.POST, instance=receta) # Aquí no hay 'request.FILES' porque quitamos el campo imagen
            if form.is_valid():
                form.save()
                messages.success(request, "Receta actualizada exitosamente.")
                return redirect('dashboard')
            else:
                messages.error(request, "Error al actualizar la receta. Revisa el formulario.")
        elif 'agregar_ingrediente' in request.POST:
            ingrediente_form = IngredienteForm(request.POST)
            if ingrediente_form.is_valid():
                ingrediente = ingrediente_form.save(commit=False)
                ingrediente.receta = receta
                ingrediente.save()
                messages.success(request, "Ingrediente agregado exitosamente.")
            else:
                messages.error(request, "Error al agregar el ingrediente.")

    form = RecetaForm(instance=receta)
    ingredientes = receta.ingredientes.all()
    ingrediente_form = IngredienteForm(initial={'receta': receta})

    return render(request, 'crear_receta_y_ingredientes.html', {
        'receta_form': form,
        'receta': receta,
        'ingredientes': ingredientes,
        'ingrediente_form': ingrediente_form
    })

@login_required
def eliminar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id, autor=request.user)
    receta.delete()
    messages.success(request, "Receta eliminada exitosamente.")
    return redirect('dashboard_usuario')

@login_required
def editar_ingrediente(request, ingrediente_id):

    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    receta = ingrediente.receta
    if receta.autor != request.user:
        messages.error(request, "No tienes permiso para editar este ingrediente.")
        return redirect('dashboard_usuario')

    if request.method == 'POST':
        form = IngredienteForm(request.POST, instance=ingrediente)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingrediente actualizado exitosamente.")
            return redirect('detalle_receta', pk=receta.id)
        else:
            messages.error(request, "Error al actualizar el ingrediente.")
    else:
        form = IngredienteForm(instance=ingrediente)

    return render(request, 'editar_ingrediente.html', {
        'form': form,
        'ingrediente': ingrediente,
        'receta': receta
    })

@login_required
def eliminar_ingrediente(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
    receta = ingrediente.receta

    if receta.autor == request.user:
        ingrediente.delete()
        messages.success(request, "Ingrediente eliminado exitosamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este ingrediente.")

    return redirect('detalle_receta', pk=receta.id)

@login_required
def quitar_favorito(request, receta_id):

    favorito = Favorito.objects.filter(usuario=request.user, receta__id=receta_id).first()
    if favorito:
        favorito.delete()
        messages.success(request, "Receta eliminada de favoritos.")
    return redirect('ver_favoritos')

def detalle_receta(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    ingredientes = receta.ingredientes.all()
    return render(request, 'detalle_receta.html', {
        'receta': receta,
        'ingredientes': ingredientes
    })