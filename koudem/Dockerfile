
# FROM python:3.10

# ENV PYTHONUNBUFFERED 1

# WORKDIR /django

# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

# COPY . .

# CMD gunicorn koudem.wsgi.application --bind 0.0.0.0:8000

# EXPOSE 8000


#===============================================================

# FROM python:3.10

# # Evitar que Python genere archivos pyc
# ENV PYTHONUNBUFFERED 1

# # Crear y establecer el directorio de trabajo
# RUN mkdir /code
# WORKDIR /code

# # Copiar los archivos de requisitos y luego instalar las dependencias
# COPY requirements.txt /code/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copiar el resto del código de la aplicación
# COPY . /code/

# # Comando para ejecutar Gunicorn
# CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":8000", "--chdir", "koudem", "koudem.wsgi:application"]


# Usa una imagen base oficial de Python
FROM python:3.11

# Define el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que correrá la app
EXPOSE 8000

# Define el comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
