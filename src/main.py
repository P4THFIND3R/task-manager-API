import uvicorn
from fastapi import FastAPI, Request, Response

from src.api.endpoints.users import router as user_router
from src.api.endpoints.tasks import router as task_router
from src.auth.router import router as auth_router
from src.log.logger import logger

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)


async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)


app.middleware('http')(catch_exceptions)

if __name__ == '__main__':
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="critical")
