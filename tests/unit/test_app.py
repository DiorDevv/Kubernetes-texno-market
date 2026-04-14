# tests/unit/test_app.py

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


class TestHealthEndpoint:

    def test_health_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["xizmat"] == "texno-market"


class TestTolovEndpoint:

    TOGRI_KARTA = 4532015112830366

    def test_togri_tolov(self):
        response = client.post(
            "/api/v1/tolov",
            json={"summa": 50_000, "karta_raqam": self.TOGRI_KARTA},
        )
        assert response.status_code == 200
        data = response.json()
        assert "tasdiqlandi" in data["xabar"]
        assert data["summa"] == 50_000

    def test_kichik_summa_rad_etiladi(self):
        response = client.post(
            "/api/v1/tolov",
            json={"summa": 500, "karta_raqam": self.TOGRI_KARTA},
        )
        assert response.status_code == 400
        assert "Minimal" in response.json()["detail"]

    def test_katta_summa_rad_etiladi(self):
        response = client.post(
            "/api/v1/tolov",
            json={"summa": 50_000_000, "karta_raqam": self.TOGRI_KARTA},
        )
        assert response.status_code == 400
        assert "Maksimal" in response.json()["detail"]

    def test_notogri_karta_rad_etiladi(self):
        response = client.post(
            "/api/v1/tolov",
            json={"summa": 50_000, "karta_raqam": 1234567890123456},
        )
        assert response.status_code == 400

    def test_qisqa_karta_rad_etiladi(self):
        response = client.post(
            "/api/v1/tolov",
            json={"summa": 50_000, "karta_raqam": 12345},
        )
        assert response.status_code == 400


class TestBuyurtmaEndpoint:

    MAHSULOTLAR = [{"id": 1, "nomi": "Telefon", "narx": 500_000, "soni": 2}]

    def test_buyurtma_yaratish(self):
        response = client.post(
            "/api/v1/buyurtma",
            json={
                "foydalanuvchi_id": 1,
                "mahsulotlar": self.MAHSULOTLAR,
                "manzil": "Toshkent",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["buyurtma_id"] is not None
        assert data["holati"] == "yangi"
        assert data["jami_summa"] == 1_000_000

    def test_buyurtma_olish(self):
        yaratish = client.post(
            "/api/v1/buyurtma",
            json={
                "foydalanuvchi_id": 1,
                "mahsulotlar": self.MAHSULOTLAR,
                "manzil": "Toshkent",
            },
        )
        buyurtma_id = yaratish.json()["buyurtma_id"]
        response = client.get(f"/api/v1/buyurtma/{buyurtma_id}")
        assert response.status_code == 200

    def test_buyurtma_topilmadi(self):
        response = client.get("/api/v1/buyurtma/9999")
        assert response.status_code == 404
        assert "topilmadi" in response.json()["detail"]

    def test_bosh_mahsulotlar_rad_etiladi(self):
        response = client.post(
            "/api/v1/buyurtma",
            json={
                "foydalanuvchi_id": 1,
                "mahsulotlar": [],
                "manzil": "Toshkent",
            },
        )
        assert response.status_code == 400

    def test_bosh_manzil_rad_etiladi(self):
        response = client.post(
            "/api/v1/buyurtma",
            json={
                "foydalanuvchi_id": 1,
                "mahsulotlar": self.MAHSULOTLAR,
                "manzil": "   ",
            },
        )
        assert response.status_code == 400


class TestChegirmaEndpoint:

    def test_chegirma_hisoblash(self):
        response = client.post(
            "/api/v1/chegirma",
            json={"narx": 100_000, "foiz": 10},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["asl_narx"] == 100_000
        assert data["chegirma_foizi"] == 10
        assert data["yangi_narx"] == 90_000

    def test_nol_chegirma(self):
        response = client.post(
            "/api/v1/chegirma",
            json={"narx": 200_000, "foiz": 0},
        )
        assert response.status_code == 200
        assert response.json()["yangi_narx"] == 200_000

    def test_manfiy_narx_rad_etiladi(self):
        response = client.post(
            "/api/v1/chegirma",
            json={"narx": -1000, "foiz": 10},
        )
        assert response.status_code == 400

    def test_100_dan_oshiq_foiz_rad_etiladi(self):
        response = client.post(
            "/api/v1/chegirma",
            json={"narx": 100_000, "foiz": 150},
        )
        assert response.status_code == 400
