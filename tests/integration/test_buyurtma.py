# tests/integration/test_buyurtma.py

import pytest
from src.buyurtma import BuyurtmaXizmati


class TestBuyurtmaIntegratsiya:

    def setup_method(self):
        self.xizmat = BuyurtmaXizmati()
        self.mahsulotlar = [
            {"id": 101, "nomi": "iPhone 15",  "narx": 12_000_000, "soni": 1},
            {"id": 205, "nomi": "Chexol",     "narx": 50_000,     "soni": 2},
        ]

    # ── Yaratish ────────────────────────────────────
    def test_buyurtma_yaratish(self):
        buyurtma = self.xizmat.yaratish(
            foydalanuvchi_id=1,
            mahsulotlar=self.mahsulotlar,
            manzil="Toshkent, Chilonzor 5",
        )
        assert buyurtma.id is not None
        assert buyurtma.holati == "yangi"
        assert buyurtma.jami_summa == 12_100_000   # 12M + 2×50k
        assert buyurtma.foydalanuvchi_id == 1

    def test_buyurtma_bazaga_saqlangani(self):
        buyurtma = self.xizmat.yaratish(
            foydalanuvchi_id=2,
            mahsulotlar=self.mahsulotlar,
            manzil="Samarqand",
        )
        # Qayta o'qish
        saqlangan = self.xizmat.olish(buyurtma.id)
        assert saqlangan is not None
        assert saqlangan.manzil == "Samarqand"

    def test_har_buyurtma_unikal_id(self):
        b1 = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        b2 = self.xizmat.yaratish(2, self.mahsulotlar, "Namangan")
        assert b1.id != b2.id

    # ── Holat yangilash ─────────────────────────────
    def test_holat_yangilash(self):
        buyurtma = self.xizmat.yaratish(1, self.mahsulotlar, "Toshkent")
        natija   = self.xizmat.holat_yangilash(buyurtma.id, "yetkazilmoqda")
        assert natija is True
        assert self.xizmat.olish(buyurtma.id).holati == "yetkazilmoqda"

    def test_mavjud_bolmagan_buyurtma_holati(self):
        natija = self.xizmat.holat_yangilash(9999, "yetkazildi")
        assert natija is False

    # ── Xato holatlar ───────────────────────────────
    def test_bosh_mahsulotlar(self):
        with pytest.raises(ValueError, match="kamida bitta"):
            self.xizmat.yaratish(1, [], "Toshkent")

    def test_bosh_manzil(self):
        with pytest.raises(ValueError, match="bo'sh"):
            self.xizmat.yaratish(1, self.mahsulotlar, "   ")

    def test_mavjud_bolmagan_buyurtma(self):
        assert self.xizmat.olish(9999) is None