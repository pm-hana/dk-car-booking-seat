FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run은 환경 변수 PORT를 주입하므로, 런타임에 이를 바인딩합니다.
# 프록시 뒤에서의 안정성을 위해 headless/CORS/XSRF 플래그를 명시적으로 지정합니다.
CMD sh -c "streamlit run app.py \
    --server.port=\${PORT:-8080} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false"
