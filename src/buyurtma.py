# src/buyurtma.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Buyurtma:
    foydalanuvchi_id: int
    mahsulotlar:      list
    manzil:           str
    id:               Optional[int]   = None
    holati:           str             = "yangi"
    jami_summa:       float           = 0.0
    yaratilgan_vaqt:  datetime        = field(
        default_factory=datetime.now
    )


class BuyurtmaXizmati:
    """
    Buyurtmalarni yaratish va boshqarish.
    """

    def __init__(self, db=None):
        # Haqiqiy loyihada bu SQLAlchemy session bo'ladi
        self.db       = db
        self._saqlash = {}   # Test uchun oddiy lug'at
        self._keyingi_id = 1

    def yaratish(
        self,
        foydalanuvchi_id: int,
        mahsulotlar:      list,
        manzil:           str,
    ) -> Buyurtma:
        """
        Yangi buyurtma yaratadi va bazaga saqlaydi.
        """
        if not mahsulotlar:
            raise ValueError("Buyurtmada kamida bitta mahsulot bo'lishi kerak")

        if not manzil.strip():
            raise ValueError("Manzil bo'sh bo'lishi mumkin emas")

        jami = sum(
            m.get("narx", 0) * m.get("soni", 1)
            for m in mahsulotlar
        )

        buyurtma = Buyurtma(
            id=self._keyingi_id,
            foydalanuvchi_id=foydalanuvchi_id,
            mahsulotlar=mahsulotlar,
            manzil=manzil,
            jami_summa=jami,
        )

        self._saqlash[buyurtma.id] = buyurtma
        self._keyingi_id += 1
        return buyurtma

    def olish(self, buyurtma_id: int) -> Optional[Buyurtma]:
        """Buyurtmani ID bo'yicha oladi."""
        return self._saqlash.get(buyurtma_id)

    def holat_yangilash(self, buyurtma_id: int, yangi_holat: str) -> bool:
        """Buyurtma holatini yangilaydi."""
        buyurtma = self.olish(buyurtma_id)
        if not buyurtma:
            return False
        buyurtma.holati = yangi_holat
        return True