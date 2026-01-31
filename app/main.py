# app/main.py

import os
from fastapi import FastAPI, Body, HTTPException, Header
from fastapi.responses import Response

from app.pdf_generator import generar_pdf

app = FastAPI(title="LibrIA PDF Service", version="1.0.0")


# ============================================================
# SEGURIDAD SIMPLE (API KEY)
# ============================================================
# * Si existe la variable de entorno PDF_API_KEY:
#     - /pdf exige el header: x-api-key
# * Si NO existe PDF_API_KEY:
#     - /pdf funciona sin autenticación (modo dev / pruebas)
# * /health siempre es público (sirve para warm-up / monitoreo)
# ============================================================

def validar_api_key(x_api_key: str | None):
    """
    Valida el header x-api-key si PDF_API_KEY está configurada.
    """
    expected = os.getenv("PDF_API_KEY")
    if expected:  # solo valida si está configurada en el entorno
        if not x_api_key or x_api_key != expected:
            raise HTTPException(status_code=401, detail="Invalid API key")

@app.head("/health")
@app.get("/health")
def health():
    return {"ok": True, "service": "libria-pdf", "status": "up"}


@app.post("/pdf")
def pdf_endpoint(
    payload: dict = Body(...),
    x_api_key: str | None = Header(default=None)
):
    """
    Espera el JSON completo de la ficha (ficha_data) y retorna un PDF (binary).

    Seguridad:
    - Si existe PDF_API_KEY en el entorno, exige header: x-api-key
    """
    # ✅ Validar API Key (solo si está configurada en Render)
    validar_api_key(x_api_key)

    try:
        pdf_bytes = generar_pdf(payload)
        if not pdf_bytes or len(pdf_bytes) < 1000:
            raise ValueError("PDF generado vacío o demasiado pequeño.")

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="libria_resena.pdf"'
            }
        )

    except HTTPException:
        # Si el error ya es HTTPException, lo re-lanzamos tal cual
        raise

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

