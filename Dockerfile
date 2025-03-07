
# FROM python:3.10

# ENV PYTHONUNBUFFERED 1

# WORKDIR /django

# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

# COPY . .

# CMD gunicorn koudem.wsgi.application --bind 0.0.0.0:8000

# EXPOSE 8000


#===============================================================

FROM python:3.10


# Evitar que Python genere archivos pyc
ENV PYTHONUNBUFFERED 1

# Crear y establecer el directorio de trabajo
RUN mkdir /code
WORKDIR /code

# Copiar los archivos de requisitos y luego instalar las dependencias
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . /code/

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "koudem", "koudem.wsgi:application"]


#===============================================



# FROM python:3.10-slim

# # Metadatos opcionales
# LABEL maintainer="tu_email@example.com"

# # Evitar que Python genere archivos pyc
# ENV PYTHONUNBUFFERED 1

# # Instalar dependencias del sistema necesarias
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# # Crear y establecer el directorio de trabajo
# RUN mkdir /code
# WORKDIR /code

# # Copiar los archivos de requisitos y luego instalar las dependencias
# COPY requirements.txt /code/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el resto del código de la aplicación
# COPY . /code/

# # Exponer el puerto 8000
# EXPOSE 8000

# # Comando para aplicar las migraciones y luego iniciar Gunicorn
# CMD ["sh", "-c", "python manage.py migrate && gunicorn -c config/gunicorn/conf.py --bind :8000 --chdir koudem koudem.wsgi:application"]
