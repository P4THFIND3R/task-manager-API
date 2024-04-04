import uvicorn
from fastapi import FastAPI

from src.api.endpoints.users import router as user_router
from src.auth.router import router as auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
