FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только requirements.txt для кэширования слоев
COPY requirements.txt /app/

# Устанавливаем зависимости системы, необходимые для Python и MinIO
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Убедитесь, что у main.py есть права на выполнение
RUN chmod +x /app/app/main.py

# Устанавливаем команду по умолчанию
CMD ["python", "app/main.py"]
