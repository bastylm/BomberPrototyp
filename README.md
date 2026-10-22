# BomberPrototyp — instancia de demostración

Copia independiente del sistema para una demostración pública en `demo.sigbomberosmulchen.cl`.

## Datos y privacidad

Este repositorio parte con historial Git nuevo. No contiene la base de datos, archivos cargados ni el `.env` del sistema actual. Carga únicamente datos y archivos ficticios en la instancia de demo.

## Preparación

1. Crea un entorno virtual de Python e instala `requirements.txt`.
2. Copia `.env.example` a `.env` y configura una nueva `SECRET_KEY`, el dominio de demo y credenciales para una base de datos y usuario dedicados.
3. Nunca reutilices la base de datos, usuario de base de datos, carpeta de archivos, credenciales SMTP o clave Django de producción.
4. Ejecuta `python manage.py migrate` y luego `python manage.py seed_demo`. El comando pide un correo y una contraseña nueva para el administrador, y crea los registros ficticios.
5. Ejecuta `python manage.py collectstatic` y configura el servicio de aplicación y proxy inverso para el subdominio.

El backend de correo predeterminado registra los mensajes localmente. No actives SMTP hasta configurar un buzón dedicado a la demo.
