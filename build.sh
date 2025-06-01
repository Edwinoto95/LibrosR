#!/usr/bin/env bash

# Salir si ocurre algún error
set -o errexit

echo "Actualizando pip..."
pip install --upgrade pip
echo "Instalando dependencias..."
pip install -r requirements.txt
echo "Ejecutando migraciones..."
python manage.py migrate --noinput
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
echo "Build completado correctamente."
