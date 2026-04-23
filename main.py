from fastapi import FastAPI, HTTPException
from models import PerevalSubmitData
from database import PerevalDatabase
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pereval API", description="API для добавления перевалов")


@app.post("/submitData")
async def submit_data(pereval: PerevalSubmitData):
    """
    Добавляет новый перевал в базу данных.
    """
    db = PerevalDatabase()
    try:
        db.connect()
        pereval_dict = pereval.dict()
        pereval_id = db.add_pereval(pereval_dict)

        return {
            "status": 200,
            "message": "Успех",
            "id": pereval_id
        }

    except Exception as e:
        logger.error(f"Ошибка при добавлении перевала: {e}")
        if db.conn:
            db.conn.rollback()
        return {
            "status": 500,
            "message": f"Ошибка сервера: {str(e)}",
            "id": None
        }
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Pereval API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)