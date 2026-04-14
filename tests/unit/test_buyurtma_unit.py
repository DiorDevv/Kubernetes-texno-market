# tests/unit/test_buyurtma_unit.py

import pytest

from src.buyurtma import BuyurtmaXizmati


class TestBuyurtmaXizmatiUnit:

    def setup_method(self):
        self.xizmat = BuyurtmaXizmati()
        self.mahsulotlar = [
            {"id": 1, "nomi": "Telefon", "narx": 5_000_000, "soni": 1},
            {"id": 2, "nomi": "Chexol", "narx": 50_000, "soni": 2},
        ]

    # ── Yaratish ────────────────────────────────────
    def test_buyurtma_yaratish_muvaffaqiyatli(self):
        buyurtma = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        assert buyurtma.id == 1
        assert buyurtma.holati == "yangi"
        assert buyurtma.foydalanuvchi_id == 1
        assert buyurtma.manzil == "Toshkent"

    def test_jami_summa_hisoblanadi(self):
        buyurtma = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        assert buyurtma.jami_summa == 5_100_000  # 5M + 2×50k

    def test_id_ketma_ket_oshadi(self):
        b1 = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        b2 = self.xizmat.yaratish(2, self.mahsulotlar, "Namangan")
        assert b1.id == 1
        assert b2.id == 2

    def test_bosh_mahsulotlar_xato(self):
        with pytest.raises(ValueError, match="kamida bitta"):
            self.xizmat.yaratish(1, [], "Toshkent")

    def test_bosh_manzil_xato(self):
        with pytest.raises(ValueError, match="bo'sh"):
            self.xizmat.yaratish(1, self.mahsulotlar, "   ")

    # ── Olish ───────────────────────────────────────
    def test_olish_mavjud_buyurtma(self):
        buyurtma = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        natija = self.xizmat.olish(buyurtma.id)
        assert natija is not None
        assert natija.id == buyurtma.id

    def test_olish_mavjud_emas(self):
        assert self.xizmat.olish(9999) is None

    # ── Holat yangilash ─────────────────────────────
    def test_holat_yangilash_muvaffaqiyatli(self):
        buyurtma = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        natija = self.xizmat.holat_yangilash(buyurtma.id, "yetkazilmoqda")
        assert natija is True
        assert self.xizmat.olish(buyurtma.id).holati == "yetkazilmoqda"

    def test_holat_yangilash_mavjud_emas(self):
        assert self.xizmat.holat_yangilash(9999, "yetkazildi") is False

    def test_narx_yoq_mahsulot(self):
        mahsulotlar = [{"id": 1, "nomi": "Test"}]  # narx va soni yo'q
        buyurtma = self.xizmat.yaratish(1, mahsulotlar, "Toshkent")
        assert buyurtma.jami_summa == 0
