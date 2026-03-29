# tests/unit/test_payment.py

import pytest
from src.payment import TolovXizmati


class TestTolovXizmati:

    def setup_method(self):
        self.tolov = TolovXizmati()
        # Luhn algoritmidan o'tadigan haqiqiy test karta
        self.togri_karta = 4532015112830366

    # ── Muvaffaqiyatli holatlar ──────────────────────
    def test_togri_tolov(self):
        ok, xabar = self.tolov.tolov_tasdiqlash(50_000, self.togri_karta)
        assert ok is True
        assert "tasdiqlandi" in xabar

    def test_minimal_summa(self):
        ok, _ = self.tolov.tolov_tasdiqlash(1_000, self.togri_karta)
        assert ok is True

    def test_maksimal_summa(self):
        ok, _ = self.tolov.tolov_tasdiqlash(10_000_000, self.togri_karta)
        assert ok is True

    # ── Summa xatolari ──────────────────────────────
    def test_kichik_summa(self):
        ok, xabar = self.tolov.tolov_tasdiqlash(500, self.togri_karta)
        assert ok is False
        assert "Minimal" in xabar

    def test_katta_summa(self):
        ok, xabar = self.tolov.tolov_tasdiqlash(50_000_000, self.togri_karta)
        assert ok is False
        assert "Maksimal" in xabar

    # ── Karta xatolari ──────────────────────────────
    def test_qisqa_karta(self):
        ok, xabar = self.tolov.tolov_tasdiqlash(50_000, 12345)
        assert ok is False
        assert "16" in xabar

    def test_notogri_luhn(self):
        # Luhn algoritmidan o'tmaydigan karta
        ok, xabar = self.tolov.tolov_tasdiqlash(50_000, 1234567890123456)
        assert ok is False
        assert "yaroqsiz" in xabar


    # ── Luhn algoritmi ──────────────────────────────
    def test_luhn_togri_karta(self):
        assert self.tolov._luhn_tekshir(4532015112830366) is True

    def test_luhn_notogri_karta(self):
        assert self.tolov._luhn_tekshir(1234567890123456) is False