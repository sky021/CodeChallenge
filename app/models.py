from sqlalchemy import Column, Integer, String
from app.database import Base

class BusinessSymptom(Base):
    __tablename__ = "business_symptoms"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(String)
    business_name = Column(String)
    symptom_code = Column(String)
    symptom_name = Column(String)
    diagnostic = Column(String)
