from fastapi import FastAPI
from controllers.student_controller import router

app = FastAPI()

app.include_router(router)