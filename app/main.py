# app/main.py

from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import Response
from app.pdf_generator import generar_pdf

app = FastAPI(title="LibrIA PDF Service", version="1.0.0")


@app.get("/health")
def health():
    return {"ok": True, "service": "libria-pdf", "status": "up"}


@app.post("/pdf")
def pdf_endpoint(payload: dict = Body(...)):
    """
    Espera el JSON completo de la ficha (ficha_data) y retorna un PDF (binary).
    """
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
