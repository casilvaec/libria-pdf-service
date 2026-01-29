# LibrIA PDF Service

Servicio en FastAPI que genera un PDF (binary) a partir de una ficha JSON.

## Endpoints
- GET /health
- POST /pdf  -> devuelve application/pdf

## Ejecutar local
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

Probar Windows
curl.exe http://localhost:8000/health

curl.exe -X POST "http://localhost:8000/pdf" `
  -H "Content-Type: application/json" `
  --data-binary "@payload.json" `
  --output salida.pdf

