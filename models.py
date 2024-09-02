from sqlalchemy import Column, Integer, String, Boolean, Date, Time
from license_server.database import Base

class Item(Base):
  __tablename__ = 'licences'
    
  cust_id                 = Column(Integer, autoincrement=True, primary_key=True, index=True)
  cust_name               = Column(String, nullable=False)
  license_number          = Column(String, nullable=False)
  license_type            = Column(String, nullable=False)
  license_activarion_day  = Column(Date, default=None)
  license_expiration_day  = Column(Date, default=None)
  license_status          = Column(Boolean, nullable=False, default=False)