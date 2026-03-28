# 🚀 Texno-Market — Full Backend System (FastAPI + DevOps)

## 📌 Loyiha haqida

**Texno-Market** — bu zamonaviy backend tizim bo‘lib, quyidagilarni o‘z ichiga oladi:

* ⚡ FastAPI asosida REST API
* 🧠 Biznes logika (to‘lov, buyurtma, chegirma)
* 🧪 Unit / Integration / E2E testlar
* 🐳 Docker + Docker Compose
* ☸️ Kubernetes deploy
* 🔄 To‘liq CI/CD pipeline (GitHub Actions)
* 📊 Monitoring (Prometheus + Grafana)
* 🔐 Security scanning (Bandit, Safety, Trivy)

---

## 🏗️ Arxitektura

```
Client → FastAPI → Business Logic → (DB + Redis)
                        ↓
                   Monitoring
            (Prometheus + Grafana)
```

---

## 📁 Loyiha tuzilmasi

```
texno-market/
├── src/            # Asosiy backend logika
├── tests/          # Testlar (unit, integration, e2e)
├── k8s/            # Kubernetes config
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/
```

---

## ⚙️ O‘rnatish (Local)

### 1️⃣ Repository clone qilish

```bash
git clone <repo_url>
cd texno-market
```

---

### 2️⃣ Docker orqali ishga tushirish

```bash
docker-compose up --build
```

👉 Ilova ishlaydi:

* API → http://localhost:8000
* Grafana → http://localhost:3000
* Prometheus → http://localhost:9090

---

### 3️⃣ Swagger UI

```bash
http://localhost:8000/docs
```

---

## 🔌 API Endpointlar

### 🟢 Health check

```http
GET /health
```

---

### 💳 To‘lov

```http
POST /api/v1/tolov
```

Body:

```json
{
  "summa": 50000,
  "karta_raqam": 4532015112830366
}
```

---

### 📦 Buyurtma

```http
POST /api/v1/buyurtma
```

```json
{
  "foydalanuvchi_id": 1,
  "mahsulotlar": [
    {"id": 1, "narx": 500000, "soni": 1}
  ],
  "manzil": "Toshkent"
}
```

---

### 💸 Chegirma

```http
POST /api/v1/chegirma
```

```json
{
  "narx": 200000,
  "foiz": 20
}
```

---

## 🧪 Testlar

### Unit testlar

```bash
pytest tests/unit/
```

### Integration testlar

```bash
pytest tests/integration/
```

### E2E testlar

```bash
pytest tests/e2e/
```

---

## 🐳 Docker

### Image build

```bash
docker build -t texno-market .
```

### Run

```bash
docker run -p 8000:8000 texno-market
```

---

## ☸️ Kubernetes Deploy

### Deploy qilish

```bash
kubectl apply -f k8s/
```

### Tekshirish

```bash
kubectl get pods -n production
```

---

## 🔄 CI/CD Pipeline

Pipeline bosqichlari:

1. ✅ Lint (black, flake8, isort, mypy)
2. ✅ Unit tests
3. ✅ Integration tests
4. ✅ E2E tests
5. 🔐 Security scan (bandit, safety)
6. 🐳 Docker build + push
7. 🚀 Staging deploy
8. 🌍 Production deploy + monitoring

---

## 📊 Monitoring

### Grafana

* URL: http://localhost:3000
* Login: `admin / admin123`

### Prometheus

* URL: http://localhost:9090

---

## 🔐 Xavfsizlik

* Bandit → kod tekshiruvi
* Safety → dependency tekshiruvi
* Trivy → Docker image scan
* Gitleaks → secret detection

---

## ⚡ Muhim texnologiyalar

* FastAPI
* PostgreSQL
* Redis
* Docker
* Kubernetes
* GitHub Actions
* Prometheus
* Grafana

---



---

## 🏁 Xulosa

Bu loyiha:

* real production darajada
* scalable
* test coverage yuqori
* CI/CD avtomatlashtirilgan

👉 Backend + DevOps ni o‘rganish uchun ideal loyiha 🚀
