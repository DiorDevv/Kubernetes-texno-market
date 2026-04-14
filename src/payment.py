# src/payment.py


class TolovXizmati:
    """
    To'lovni tasdiqlash va boshqarish xizmati.
    """

    def __init__(self):
        self.minimal_summa = 1_000  # 1,000 so'm
        self.maksimal_summa = 10_000_000  # 10,000,000 so'm

    def tolov_tasdiqlash(self, summa: int, karta_raqam: int) -> tuple[bool, str]:
        """
        To'lovni tasdiqlaydi.

        Returns:
            (True, "xabar")  — muvaffaqiyatli
            (False, "xabar") — xato
        """

        # 1. Summa tekshiruvi
        if summa < self.minimal_summa:
            return False, f"Minimal summa {self.minimal_summa} so'm"

        if summa > self.maksimal_summa:
            return False, f"Maksimal summa {self.maksimal_summa} so'm"

        # 2. Karta uzunligi
        if len(str(karta_raqam)) != 16:
            return False, "Karta raqami 16 ta raqamdan iborat bo'lishi kerak"

        # 3. Luhn algoritmi
        if not self._luhn_tekshir(karta_raqam):
            return False, "Karta raqami yaroqsiz"

        return True, "To'lov tasdiqlandi ✅"

    def _luhn_tekshir(self, raqam: int) -> bool:
        """
        Karta raqamini Luhn algoritmi bilan tekshiradi.
        Barcha haqiqiy kredit karta raqamlari bu testdan o'tadi.
        """
        raqamlar = [int(r) for r in str(raqam)]
        raqamlar.reverse()

        jami = 0
        for i, r in enumerate(raqamlar):
            if i % 2 == 1:
                r *= 2
                if r > 9:
                    r -= 9
            jami += r

        return jami % 10 == 0
