from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib import messages
from django.db import connection
from .models import Libro, Autor, Editorial

USUARIO = 'admin_secure_user'
CONTRASEÑA = 'S3guraP@ssw0rd!2025'

def add_unique_message(request, level, message):
    """Agrega mensajes únicos para evitar duplicados en Django messages."""
    # Permitir usar 'exito' en español como alias de 'success'
    if level == 'exito':
        level = 'success'
    existing_messages = [str(m.message) for m in messages.get_messages(request)]
    if message not in existing_messages:
        if hasattr(messages, level):
            getattr(messages, level)(request, message)
        else:
            messages.info(request, message)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR')
        cache_key = f'login_attempts_{ip}'
        intentos = cache.get(cache_key, 0)

        if intentos >= 3:
            add_unique_message(request, 'error', '🔒 Demasiados intentos fallidos. Espere 1 minuto.')
            return render(request, 'login.html')

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == USUARIO and password == CONTRASEÑA:
            cache.delete(cache_key)
            user, created = User.objects.get_or_create(username=USUARIO)
            if created or not user.check_password(CONTRASEÑA):
                user.set_password(CONTRASEÑA)
                user.save()
            login(request, user)
            return redirect('inicio')
        else:
            cache.set(cache_key, intentos + 1, 60)
            add_unique_message(request, 'error', '❌ Credenciales incorrectas')
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def reporte_view(request):
    libros = Libro.objects.select_related('autor', 'editorial').all()
    return render(request, 'reporte.html', {'libros': libros})

@login_required
def inicio(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT nombre_aut, COUNT(id_lib) AS total_libros
            FROM Autores
            LEFT JOIN Libros USING (id_aut)
            GROUP BY nombre_aut
            ORDER BY total_libros DESC
        """)
        autores = cursor.fetchall()
        labels_autores = [row[0] for row in autores]
        data_autores = [row[1] for row in autores]

        cursor.execute("""
            SELECT genero_lib, COUNT(*) AS total_libros
            FROM Libros
            GROUP BY genero_lib
            ORDER BY total_libros DESC
            LIMIT 1
        """)
        genero_top1 = cursor.fetchall()
        labels_genero_top1 = [row[0] for row in genero_top1]
        data_genero_top1 = [row[1] for row in genero_top1]

        cursor.execute("""
            SELECT genero_lib, COUNT(*) AS total_libros
            FROM Libros
            GROUP BY genero_lib
            ORDER BY total_libros DESC
            LIMIT 3
        """)
        generos_top3 = cursor.fetchall()
        labels_generos_top3 = [row[0] for row in generos_top3]
        data_generos_top3 = [row[1] for row in generos_top3]

        cursor.execute("""
            SELECT e.nombre_edi, COUNT(l.id_lib) AS total_libros
            FROM Editoriales e
            JOIN Libros l ON e.id_edi = l.id_edi
            GROUP BY e.nombre_edi
            ORDER BY total_libros DESC
            LIMIT 1
        """)
        editorial_top1 = cursor.fetchall()
        labels_editorial_top1 = [row[0] for row in editorial_top1]
        data_editorial_top1 = [row[1] for row in editorial_top1]

        cursor.execute("""
            SELECT e.nombre_edi, COUNT(l.id_lib) AS total_libros
            FROM Editoriales e
            JOIN Libros l ON e.id_edi = l.id_edi
            GROUP BY e.nombre_edi
            ORDER BY total_libros DESC
            LIMIT 3
        """)
        editoriales_top3 = cursor.fetchall()
        labels_editoriales_top3 = [row[0] for row in editoriales_top3]
        data_editoriales_top3 = [row[1] for row in editoriales_top3]

        cursor.execute("""
            SELECT año_lib, COUNT(*) AS total_libros
            FROM Libros
            GROUP BY año_lib
            ORDER BY año_lib
        """)
        años = cursor.fetchall()
        labels_años = [row[0] for row in años]
        data_años = [row[1] for row in años]

    context = {
        'labels_autores': labels_autores,
        'data_autores': data_autores,
        'labels_genero_top1': labels_genero_top1,
        'data_genero_top1': data_genero_top1,
        'labels_generos_top3': labels_generos_top3,
        'data_generos_top3': data_generos_top3,
        'labels_editorial_top1': labels_editorial_top1,
        'data_editorial_top1': data_editorial_top1,
        'labels_editoriales_top3': labels_editoriales_top3,
        'data_editoriales_top3': data_editoriales_top3,
        'labels_años': labels_años,
        'data_años': data_años,
    }
    return render(request, 'inicio.html', context)

@login_required
def lista_libros(request):
    libros = Libro.objects.select_related('autor', 'editorial').order_by('-id').all()
    return render(request, 'libroslista.html', {'libros': libros})

@login_required
def crear_libro(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        año = request.POST['año']
        genero = request.POST['genero']
        autor_id = request.POST['autor']
        editorial_id = request.POST['editorial']
        try:
            Libro.objects.create(
                titulo=titulo,
                año=año,
                genero=genero,
                autor_id=autor_id,
                editorial_id=editorial_id
            )
            add_unique_message(request, 'exito', 'Libro creado exitosamente')
        except Exception as e:
            add_unique_message(request, 'error', f'Error al crear el libro: {e}')
        return redirect('lista_libros')
    
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    return render(request, 'librosform.html', {
        'autores': autores,
        'editoriales': editoriales,
        'titulo_form': 'Crear Libro'
    })

@login_required
def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == 'POST':
        libro.titulo = request.POST['titulo']
        libro.año = request.POST['año']
        libro.genero = request.POST['genero']
        libro.autor_id = request.POST['autor']
        libro.editorial_id = request.POST['editorial']
        try:
            libro.save()
            add_unique_message(request, 'exito', 'Libro actualizado exitosamente')
        except Exception as e:
            add_unique_message(request, 'error', f'Error al actualizar el libro: {e}')
        return redirect('lista_libros')
    
    autores = Autor.objects.all()
    editoriales = Editorial.objects.all()
    return render(request, 'librosform.html', {
        'libro': libro,
        'autores': autores,
        'editoriales': editoriales,
        'titulo_form': 'Editar Libro'
    })

@login_required
def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    try:
        libro.delete()
        add_unique_message(request, 'exito', 'Libro eliminado exitosamente')
    except Exception as e:
        add_unique_message(request, 'error', f'Error al eliminar el libro: {e}')
    return redirect('lista_libros')

@login_required
def lista_autores(request):
    autores = Autor.objects.order_by('-id').all()
    return render(request, 'autoreslista.html', {'autores': autores})

@login_required
def crear_autor(request):
    if request.method == 'POST':
        nombre_autor = request.POST['nombre_autor']
        nacionalidad = request.POST['nacionalidad']
        try:
            Autor.objects.create(
                nombre_autor=nombre_autor,
                nacionalidad=nacionalidad
            )
            add_unique_message(request, 'exito', 'Autor creado exitosamente')
        except Exception as e:
            add_unique_message(request, 'error', f'Error al crear el autor: {e}')
        return redirect('lista_autores')
    
    return render(request, 'autoresform.html', {'titulo_form': 'Crear Autor'})

@login_required
def editar_autor(request, id):
    autor = get_object_or_404(Autor, id=id)
    if request.method == 'POST':
        autor.nombre_autor = request.POST['nombre_autor']
        autor.nacionalidad = request.POST['nacionalidad']
        try:
            autor.save()
            add_unique_message(request, 'exito', 'Autor actualizado exitosamente')
        except Exception as e:
            add_unique_message(request, 'error', f'Error al actualizar el autor: {e}')
        return redirect('lista_autores')
    
    return render(request, 'autoresform.html', {
        'autor': autor,
        'titulo_form': 'Editar Autor'
    })

@login_required
def eliminar_autor(request, id):
    autor = get_object_or_404(Autor, id=id)
    try:
        autor.delete()
        add_unique_message(request, 'exito', 'Autor eliminado exitosamente')
    except Exception as e:
        add_unique_message(request, 'error', f'Error al eliminar el autor: {e}')
    return redirect('lista_autores')

@login_required
def lista_editoriales(request):
    editoriales = Editorial.objects.order_by('-id').all()
    return render(request, 'editorialeslista.html', {'editoriales': editoriales})

@login_required
def crear_editorial(request):
    if request.method == 'POST':
        nombre_editorial = request.POST['nombre_editorial']
        try:
            Editorial.objects.create(nombre_editorial=nombre_editorial)
            add_unique_message(request, 'exito', 'Editorial creada exitosamente')
        except Exception as e:
            add_unique_message(request, 'error', f'Error al crear la editorial: {e}')
        return redirect('lista_editoriales')
    
    return render(request, 'editorialesform.html', {'titulo_form': 'Crear Editorial'})

@login_required
def editar_editorial(request, id):
    editorial = get_object_or_404(Editorial, id=id)
    if request.method == 'POST':
        editorial.nombre_editorial = request.POST['nombre_editorial']
        try:
            editorial.save()
            add_unique_message(request, 'exito', 'Editorial actualizada exitosamente')
        except Exception as e:
            add_unique_message(request, 'error', f'Error al actualizar la editorial: {e}')
        return redirect('lista_editoriales')
    
    return render(request, 'editorialesform.html', {
        'editorial': editorial,
        'titulo_form': 'Editar Editorial'
    })

@login_required
def eliminar_editorial(request, id):
    editorial = get_object_or_404(Editorial, id=id)
    try:
        editorial.delete()
        add_unique_message(request, 'exito', 'Editorial eliminada exitosamente')
    except Exception as e:
        add_unique_message(request, 'error', f'Error al eliminar la editorial: {e}')
    return redirect('lista_editoriales')
