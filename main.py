from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from fastapi.openapi.utils import get_openapi
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta
import psycopg2, random, string, models

########################################################
license_schema = "XXXXX-XXXXXXXXXX-XXXXX"
def generate_license_key(license_schema):
    license_key = []
    for char in license_schema:
        if char == 'X':
            license_key.append(random.choice(string.ascii_uppercase + string.digits))
        else:
            license_key.append(char)
    return ''.join(license_key)

########################################################
app = FastAPI()

# Create tables definition from model.py file
models.Base.metadata.create_all(bind=engine)

# DB Connection
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

# License generation class
class LicenseGenerate(BaseModel):
    customer_name: str
    license_generation_day: date
    license_generation_time: time
    license_type: str
    license_expiration_day: date

########################################################
# Main endpoint
@app.get("/")
async def read_api():
  return {"message": "Licensing API"}

# Get all licenses
@app.get("/licenses/get_all")
async def get_all_licenses(db: Session = Depends(get_db)):
    items = db.query(models.License).all()
    return items

# Get only active licenses
@app.get("/licenses/get_active")
async def get_active_licenses(db: Session = Depends(get_db)):
    items = db.query(models.License).filter(models.License.is_license_activated == True).all()
    return items

# Get only inactive licenses
@app.get("/licenses/get_inactive")
async def get_inactive_licenses(db: Session = Depends(get_db)):
    items = db.query(models.License).filter(models.License.is_license_activated == False).all()
    return items

# Generate license
@app.post("/license/generate")
async def generate_new_license(item: LicenseGenerate, db: Session = Depends(get_db)):
    # Generate the license key using your function
    license_key = generate_license_key(license_schema)
    # Get the current date and time
    license_generation_day = datetime.now().date()
    license_generation_time = datetime.now().time().strftime("%H:%M:%S")
    # Calculate the expiration date by adding 12 months
    license_expiration_day = license_generation_day + relativedelta(months=12)

    # Create the License model instance
    db_item = models.License(
        customer_name=item.customer_name,
        license_key=license_key,
        license_generation_day=license_generation_day,
        license_generation_time=license_generation_time,
        license_type=item.license_type,
        license_expiration_day=license_expiration_day,
        is_license_activated=False
    )
    # Save to the database
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

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