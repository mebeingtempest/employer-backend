FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    build-essential \
    libssl3 \
    libgssapi-krb5-2 \
    && rm -rf /var/lib/apt/lists/*

# Microsoft package repo for ODBC Driver 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --dearmor > /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/microsoft.list && \
    apt-get update && apt-get install -y \
    msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "app:app"]
