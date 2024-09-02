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

# Base Model for items
class Licenses(BaseModel):
  cust_id: str
  cust_name: str
  license_number: str
  license_type: str
  license_activarion_day: date
  license_expiration_day: date
  license_status: bool


# DB Connection
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/")
async def read_api():
  return {"message": "Licensing API"}

@app.get("/list_all_licenses")
async def list_all_licenses(db: Session = Depends(get_db)):
    # Define your SQL query here
    query = text("SELECT license_number FROM licences")
    
    # Execute the query
    result = db.execute(query)
    
    # Fetch all results
    rows = result.fetchall()
    
    
    return {"licenses": rows}


# Custom swagger definition, path /docs
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Przemas' API",
        version="1.0.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi