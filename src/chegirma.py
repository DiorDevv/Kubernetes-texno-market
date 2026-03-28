# src/chegirma.py

class ChegirmaXizmati:
    """
    Chegirma hisoblash xizmati.
    """

    def chegirma_hisoblash(self, narx: float, foiz: float) -> float:
        """
        Narxdan chegirma hisoblaydi.

        Args:
            narx:  Mahsulot narxi (so'm)
            foiz:  Chegirma foizi (0-100)

        Returns:
            Chegirmadan keyingi narx

        Raises:
            ValueError: Noto'g'ri qiymat kiritilsa
        """
        if narx < 0:
            raise ValueError("Narx manfiy bo'lishi mumkin emas")

        if foiz < 0:
            raise ValueError("Chegirma foizi manfiy bo'lishi mumkin emas")

        if foiz > 100:
            raise ValueError("Chegirma foizi 100 dan oshishi mumkin emas")

        chegirma_summasi = narx * (foiz / 100)
        return narx - chegirma_summasi