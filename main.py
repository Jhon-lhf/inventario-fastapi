from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base,engine
from app.routers import auth, products, users,inventory,dashboard,sales,reports

app=FastAPI(title="API de inventario")

Base.metadata.create_all(bind=engine)

origins=["http://localhost:3000",]

# Permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # <- frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(dashboard.router)
app.include_router(sales.router)
app.include_router(reports.router)