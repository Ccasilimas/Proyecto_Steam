
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt


# Instalar ngrok
RUN apt-get update && apt-get install -y curl && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc | apt-key add - && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install ngrok -y

# Copiar la aplicación FastAPI y el código Python al contenedor
COPY . /app

# Definir la variable de entorno del authtoken de ngrok 
ENV NGROK_AUTHTOKEN=2nG3jXxr5bZPfob3SazmDNBZbEf_4YNPg1Hk1sjfReRddNCT5

EXPOSE 80 4040

# Comando para iniciar FastAPI y ngrok
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 80 & ngrok http 80"] 