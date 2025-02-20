from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import os
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_dummy_prediction(row):
    return "Hit" if row["feature1"] > 50 else "Flop"

FILE_PATH = r"  "  # Make sure this is accessible

@app.get("/process-local-file/")
async def process_local_file_endpoint(db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(FILE_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found at the given path.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Ensure required columns are present
    if not {"feature1", "feature2"}.issubset(df.columns):
        raise HTTPException(status_code=400, detail="CSV must contain 'feature1' and 'feature2' columns")

    df = df.dropna(subset=["feature1", "feature2"])  # Handle missing values

    entries = []
    for _, row in df.iterrows():
        prediction = generate_dummy_prediction(row)
        entry = models.DataEntry(feature1=row["feature1"], feature2=row["feature2"], prediction=prediction)
        db.add(entry)
        entries.append({"feature1": row["feature1"], "feature2": row["feature2"], "prediction": prediction})

    db.commit()
    return {"message": "Local file processed successfully", "results": entries}

@app.post("/upload/")
async def upload_file_endpoint(db: Session = Depends(get_db)):  # Changed function name
    try:
        df = pd.read_csv(FILE_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found at the given path.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not {"feature1", "feature2"}.issubset(df.columns):
        raise HTTPException(status_code=400, detail="CSV must contain 'feature1' and 'feature2' columns")

    df = df.dropna(subset=["feature1", "feature2"])  # Handle missing values

    entries = []
    for _, row in df.iterrows():
        prediction = generate_dummy_prediction(row)
        entry = models.DataEntry(feature1=row["feature1"], feature2=row["feature2"], prediction=prediction)
        db.add(entry)
        entries.append({"feature1": row["feature1"], "feature2": row["feature2"], "prediction": prediction})

    db.commit()
    return {"message": "Data stored successfully", "results": entries}

@app.get("/results/")
async def get_results(db: Session = Depends(get_db)):
    results = db.query(models.DataEntry).all()
    return results
