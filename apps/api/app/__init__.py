# Re-export the FastAPI app so `uvicorn app.main:app` and `app` both resolve.
from app.main import app

__all__ = ["app"]
