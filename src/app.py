# src/app.py — Asosiy FastAPI ilovasi

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.buyurtma import BuyurtmaXizmati
from src.chegirma import ChegirmaXizmati
from src.payment import TolovXizmati

app = FastAPI(
    title="Texno-Market API",
    version="1.0.0",
)

# Xizmatlar
tolov_xizmati = TolovXizmati()
buyurtma_xizmati = BuyurtmaXizmati()
chegirma_xizmati = ChegirmaXizmati()


# ──────────────────────────────────
# Sog'liq tekshiruvi — CI/CD monitoring uchun
# ──────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok", "xizmat": "texno-market"}


# ──────────────────────────────────
# To'lov endpoint
# ──────────────────────────────────
class TolovSo_rov(BaseModel):
    summa: int
    karta_raqam: int


@app.post("/api/v1/tolov")
def tolov_qilish(so_rov: TolovSo_rov):
    muvaffaqiyat, xabar = tolov_xizmati.tolov_tasdiqlash(
        so_rov.summa, so_rov.karta_raqam
    )
    if not muvaffaqiyat:
        raise HTTPException(status_code=400, detail=xabar)
    return {"xabar": xabar, "summa": so_rov.summa}


# ──────────────────────────────────
# Buyurtma endpoint
# ──────────────────────────────────
class BuyurtmaSo_rov(BaseModel):
    foydalanuvchi_id: int
    mahsulotlar: list
    manzil: str


@app.post("/api/v1/buyurtma")
def buyurtma_yaratish(so_rov: BuyurtmaSo_rov):
    try:
        buyurtma = buyurtma_xizmati.yaratish(
            foydalanuvchi_id=so_rov.foydalanuvchi_id,
            mahsulotlar=so_rov.mahsulotlar,
            manzil=so_rov.manzil,
        )
        return {
            "buyurtma_id": buyurtma.id,
            "holati": buyurtma.holati,
            "jami_summa": buyurtma.jami_summa,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/buyurtma/{buyurtma_id}")
def buyurtma_olish(buyurtma_id: int):
    buyurtma = buyurtma_xizmati.olish(buyurtma_id)
    if not buyurtma:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")
    return buyurtma


# ──────────────────────────────────
# Chegirma endpoint
# ──────────────────────────────────
class ChegirmaSo_rov(BaseModel):
    narx: float
    foiz: float


@app.post("/api/v1/chegirma")
def chegirma_hisoblash(so_rov: ChegirmaSo_rov):
    try:
        natija = chegirma_xizmati.chegirma_hisoblash(so_rov.narx, so_rov.foiz)
        return {
            "asl_narx": so_rov.narx,
            "chegirma_foizi": so_rov.foiz,
            "yangi_narx": natija,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
