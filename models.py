from sqlalchemy import Column, Integer, String, Boolean, Date, Time
from database import Base

class Item(Base):
  __tablename__ = 'licenses'
    
  license_id                = Column(Integer, autoincrement=True, primary_key=True, index=True)
  customer_na               = Column(String, nullable=False)
  license_number            = Column(String, nullable=False)
  license_generation_day    = Column(Date, default=None)
  license_generation_time   = Column(Time, default=None)
  license_type              = Column(String, nullable=False)
  license_activation_day    = Column(Date, default=None)
  license_activation_time   = Column(Time, default=None)
  license_expiration_day    = Column(Date, default=None)
  is_license_activated      = Column(Boolean, nullable=False, default=False)
