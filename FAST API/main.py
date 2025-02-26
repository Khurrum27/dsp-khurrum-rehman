from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# FastAPI app
app = FastAPI()

# Database Configuration
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/DSP_project"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define ORM model for the predictions table
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    danceability = Column(Float, nullable=False)
    genre = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    prediction = Column(String, nullable=False)

# Create the database table (if not exists)
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define request model
class SongData(BaseModel):
    danceability: float
    genre: str
    artist: str

# Endpoint to receive data and store predictions
@app.post("/predict")
async def predict_songs(songs: List[SongData], db: Session = Depends(get_db)):
    try:
        predictions = []
        for song in songs:
            # Dummy prediction logic (replace with ML model if needed)
            prediction = "Hit" if song.danceability > 0.5 else "Miss"

            # Insert data using ORM
            db_prediction = Prediction(
                danceability=song.danceability,
                genre=song.genre,
                artist=song.artist,
                prediction=prediction
            )
            db.add(db_prediction)
            db.commit()
            db.refresh(db_prediction)

            predictions.append({
                "id": db_prediction.id,
                "artist": song.artist,
                "genre": song.genre,
                "prediction": prediction
            })

        return {"results": predictions}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

# Endpoint to fetch predictions
@app.get("/results")
async def get_results(db: Session = Depends(get_db)):
    try:
        results = db.query(Prediction).order_by(Prediction.id.desc()).limit(10).all()

        return {
            "results": [
                {
                    "id": row.id,
                    "artist": row.artist,
                    "genre": row.genre,
                    "prediction": row.prediction,
                    "source": row.source,
                    "created_at": row.created_at 
                }
                for row in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    print("Hello Worl Tatta Khurrum")   