from fastapi import FastAPI
from app.routes.user_route import router as user_router
from app.routes.excel_route import router as excel_router
from app.routes.pdf_route import router as pdf_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(excel_router)
app.include_router(pdf_router)

@app.get("/")
def home():
    return {
        "message": "Hello World"
    }