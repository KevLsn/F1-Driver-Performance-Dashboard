FROM python:3.12-slim

# ENV
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# SYSTEM DEPENDENCIES
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# WORKDIR
WORKDIR /app

# PYTHON DEPENDENCIES
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# APP FILES
COPY src/ src/
COPY src/app.py .

# FastF1 cache directory
RUN mkdir -p /app/cache

# STREAMLIT
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]