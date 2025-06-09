FROM python:3.11-slim

# Establece directorio de trabajo
WORKDIR /app

# Copia archivos de dependencias
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Expone el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para correr la app con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
