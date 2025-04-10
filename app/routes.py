from fastapi import APIRouter, UploadFile, File, Query, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import csv
from io import StringIO
from app.database import SessionLocal
from app.models import BusinessSymptom

router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key")

API_KEY = "123123"

def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

# CSV import endpoint
@router.post("/import-csv/", dependencies=[Depends(verify_api_key)])
async def import_csv(file: UploadFile = File(...)):
    db = SessionLocal()
    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        reader = csv.DictReader(StringIO(decoded))

        for row in reader:
            record = BusinessSymptom(
                business_id=row["Business ID"],
                business_name=row["Business Name"],
                symptom_code=row["Symptom Code"],
                symptom_name=row["Symptom Name"],
                diagnostic=row["Symptom Diagnostic"]
            )
            db.add(record)

        db.commit()
        return {"message": "CSV imported successfully"}

    except Exception as e:
        db.rollback()
        return {"error": f"Failed to import CSV: {str(e)}"}
    
    finally:
        db.close()


# Data retrieval endpoint
@router.get("/symptoms/", dependencies=[Depends(verify_api_key)])
def get_symptoms(business_id: str = Query(None), diagnostic: str = Query(None)):
    db = SessionLocal()
    try:
        query = db.query(BusinessSymptom)

        if business_id:
            query = query.filter(BusinessSymptom.business_id == business_id)
        if diagnostic:
            query = query.filter(BusinessSymptom.diagnostic == diagnostic)

        results = query.all()

        return [
            {
                "business_id": r.business_id,
                "business_name": r.business_name,
                "symptom_code": r.symptom_code,
                "symptom_name": r.symptom_name,
                "diagnostic": r.diagnostic
            }
            for r in results
        ]
    except Exception as e:
        return {"error": f"Failed to retrieve data: {str(e)}"}
    finally:
        db.close()

