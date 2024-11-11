# Usar una imagen base que soporte FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Copiar el archivo de requisitos
COPY requirements.txt /app/
RUN echo "Instalando los requisitos..." && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    echo "Requisitos instalados."

# Copiar la aplicación FastAPI y el código Python al contenedor
COPY . /app/
RUN echo "Código de la aplicación copiado."

# Exponer el puerto
EXPOSE 80
RUN echo "Puerto expuesto: 80."

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]