# Aplicaciones/repaso/models.py
from django.db import models

class Editorial(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_edi')
    nombre_editorial = models.CharField(max_length=100, db_column='nombre_edi')
    
    class Meta:
        db_table = 'Editoriales'
        managed = False  # Django no gestionará esta tabla
    
    def __str__(self):
        return self.nombre_editorial

class Autor(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_aut')
    nombre_autor = models.CharField(max_length=100, db_column='nombre_aut')
    nacionalidad = models.CharField(max_length=50, db_column='nacionalidad_aut')
    
    class Meta:
        db_table = 'Autores'
        managed = False  # Django no gestionará esta tabla
    
    def __str__(self):
        return self.nombre_autor

class Libro(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_lib')
    titulo = models.CharField(max_length=150, db_column='titulo_lib')
    año = models.IntegerField(db_column='año_lib')
    genero = models.CharField(max_length=50, db_column='genero_lib')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, db_column='id_aut')
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, db_column='id_edi')
    
    class Meta:
        db_table = 'Libros'
        managed = False  # Django no gestionará esta tabla
    
    def __str__(self):
        return self.titulo
