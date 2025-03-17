FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y gcc libpq-dev

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY . .

# Comando para ejecutar (usando Gunicorn en producción)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]