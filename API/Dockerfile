# Usar una imagen base que soporte FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Copiar el archivo de requisitos
COPY requirements.txt /app/
RUN echo "Instalando los requisitos..." && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    echo "Requisitos instalados."

# Instalar ngrok
RUN echo "Instalando ngrok..." && \
    apt-get update && apt-get install -y curl && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc | apt-key add - && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install ngrok -y && \
    echo "ngrok instalado."

# Copiar la aplicación FastAPI y el código Python al contenedor
COPY . /app/
RUN echo "Código de la aplicación copiado."

# Definir la variable de entorno del authtoken de ngrok 
# Asegúrate de no compartir tu token de ngrok.
ENV NGROK_AUTHTOKEN=2nG3jXxr5bZPfob3SazmDNBZbEf_4YNPg1Hk1sjfReRddNCT5

# Exponer puertos
EXPOSE 80 4040
RUN echo "Puertos expuestos: 8010 y 4040."

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 80 & ngrok http 80"] 