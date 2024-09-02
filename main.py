from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from fastapi.openapi.utils import get_openapi
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, time
import psycopg2

app = FastAPI()

# Create tables definition from model.py file
models.Base.metadata.create_all(bind=engine)

# Class for license generation
class License_denerate(BaseModel):
    cust_id: str
    cust_name: str
    license_number: str
    license_generation_date: date
    license_type: str
    license_expiration_day: date
    is_license_activated: bool

# DB Connection
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# Main endpoint
@app.get("/")
async def read_api():
  return {"message": "Licensing API"}

# Get all on stock items from DB
@app.get("/licenses/get_all")
async def get_all_licenses(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

# Get all on stock items from DB
@app.get("/licenses/get_active")
async def get_active_licenses(db: Session = Depends(get_db)):
    items = db.query(models.Item).filter(models.Item.is_license_activated == True).all()
    return items

@app.get("/licenses/get_inactive")
async def get_inactive_licenses(db: Session = Depends(get_db)):
    items = db.query(models.Item).filter(models.Item.is_license_activated == False).all()
    return items

# Custom swagger definition, path /docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Licensing API",
        version="1.0.0",
        description="API to handle licensing info Postgres Database",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi