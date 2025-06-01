
from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/crear/', views.crear_libro, name='crear_libro'),
    path('libros/editar/<int:id>/', views.editar_libro, name='editar_libro'),
    path('libros/eliminar/<int:id>/', views.eliminar_libro, name='eliminar_libro'),
    
  
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/crear/', views.crear_autor, name='crear_autor'),
    path('autores/editar/<int:id>/', views.editar_autor, name='editar_autor'),
    path('autores/eliminar/<int:id>/', views.eliminar_autor, name='eliminar_autor'),
    
   
    path('editoriales/', views.lista_editoriales, name='lista_editoriales'),
    path('editoriales/crear/', views.crear_editorial, name='crear_editorial'),
    path('editoriales/editar/<int:id>/', views.editar_editorial, name='editar_editorial'),
    path('editoriales/eliminar/<int:id>/', views.eliminar_editorial, name='eliminar_editorial'),


     path('reporte/', views.reporte_view, name='reporte'),
     
]