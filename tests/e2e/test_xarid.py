# tests/e2e/test_xarid.py
# Playwright orqali to'liq brauzer testi

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


class TestXaridOqimi:
    """
    To'liq xarid jarayonini real brauzer orqali tekshiradi.
    Bu testlar staging muhitida ishlaydi.
    """

    def test_health_endpoint(self, page: Page):
        """API sog'lommi?"""
        response = page.request.get(f"{BASE_URL}/health")
        assert response.status == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_togri_tolov_oqimi(self, page: Page):
        """Muvaffaqiyatli to'lov jarayoni"""
        response = page.request.post(
            f"{BASE_URL}/api/v1/tolov",
            json={
                "summa": 50_000,
                "karta_raqam": 4532015112830366,
            },
        )
        assert response.status == 200
        data = response.json()
        assert "tasdiqlandi" in data["xabar"]

    def test_notogri_tolov_rad_etiladi(self, page: Page):
        """Yomon karta rad etilishi kerak"""
        response = page.request.post(
            f"{BASE_URL}/api/v1/tolov",
            json={
                "summa": 50_000,
                "karta_raqam": 1234567890123456,
            },
        )
        assert response.status == 400

    def test_buyurtma_yaratish_oqimi(self, page: Page):
        """To'liq buyurtma jarayoni"""
        response = page.request.post(
            f"{BASE_URL}/api/v1/buyurtma",
            json={
                "foydalanuvchi_id": 1,
                "mahsulotlar": [{"id": 101, "narx": 500_000, "soni": 1}],
                "manzil": "Toshkent, Yunusobod 14",
            },
        )
        assert response.status == 200
        data = response.json()
        assert data["buyurtma_id"] is not None
        assert data["holati"] == "yangi"
        assert data["jami_summa"] == 500_000

    def test_chegirma_hisoblash_oqimi(self, page: Page):
        """Chegirma to'g'ri hisoblanadi"""
        response = page.request.post(
            f"{BASE_URL}/api/v1/chegirma",
            json={"narx": 200_000, "foiz": 20},
        )
        assert response.status == 200
        data = response.json()
        assert data["yangi_narx"] == 160_000
