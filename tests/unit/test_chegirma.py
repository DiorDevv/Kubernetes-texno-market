# tests/unit/test_chegirma.py

import pytest
from src.chegirma import ChegirmaXizmati


class TestChegirmaXizmati:

    def setup_method(self):
        self.xizmat = ChegirmaXizmati()

    # ── Muvaffaqiyatli holatlar ──────────────────────
    def test_oddiy_chegirma(self):
        natija = self.xizmat.chegirma_hisoblash(100_000, 10)
        assert natija == 90_000

    def test_chegirma_yoq(self):
        natija = self.xizmat.chegirma_hisoblash(100_000, 0)
        assert natija == 100_000

    def test_tolik_chegirma(self):
        natija = self.xizmat.chegirma_hisoblash(100_000, 100)
        assert natija == 0.0

    def test_yarim_chegirma(self):
        natija = self.xizmat.chegirma_hisoblash(200_000, 50)
        assert natija == 100_000

    # ── Xato holatlar ───────────────────────────────
    def test_manfiy_narx(self):
        with pytest.raises(ValueError, match="manfiy"):
            self.xizmat.chegirma_hisoblash(-1000, 10)

    def test_manfiy_foiz(self):
        with pytest.raises(ValueError, match="manfiy"):
            self.xizmat.chegirma_hisoblash(100_000, -5)

    def test_100_dan_oshiq_foiz(self):
        with pytest.raises(ValueError, match="100"):
            self.xizmat.chegirma_hisoblash(100_000, 150)