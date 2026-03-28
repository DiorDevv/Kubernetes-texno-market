# Dockerfile — Ilovani Docker containerga joylash

# 1-BOSQICH: Kutubxonalarni quramiz (kesh uchun alohida)
FROM python:3.11-slim AS builder

WORKDIR /build

# Faqat requirements — kesh samarali ishlashi uchun
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# 2-BOSQICH: Ishchi image (kichik, xavfsiz)
FROM python:3.11-slim AS production

# Xavfsizlik: root bo'lmagan foydalanuvchi
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Builder dan o'rnatilgan kutubxonalar
COPY --from=builder /root/.local /home/appuser/.local

# Asosiy kod
COPY src/ ./src/

# Versiya ma'lumotlari (CI dan keladi)
ARG VERSION=dev
ARG BUILD_DATE=unknown
LABEL version=$VERSION
LABEL build_date=$BUILD_DATE
LABEL maintainer="texno-market@team.uz"

# Root bo'lmagan foydalanuvchiga o'tish
USER appuser

# Port
EXPOSE 8000

# Sog'liq tekshiruvi
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Ishga tushirish
ENV PATH=/home/appuser/.local/bin:$PATH
CMD ["uvicorn", "src.app:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4"]