import uvicorn
from fastapi import FastAPI # need python-multipart
from app.views import router as status_router
from app.routes import router as data_router
from app.models import Base
from app.database import engine

#Base.metadata.create_all(bind=engine)

app = FastAPI(title="AdviNow Interview Challenge", version="1.6")

app.include_router(status_router)
app.include_router(data_router)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8013)
