import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Seed, Instrument, Plant, Subsidy

app = FastAPI(title="Farmers Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Farmers Management System API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Helper models for filters
class ContentFilter(BaseModel):
    state: Optional[str] = None
    language: Optional[str] = None
    q: Optional[str] = None

# Generic fetch helper

def _fetch_collection(name: str, state: Optional[str], language: Optional[str], q: Optional[str]):
    filter_dict = {}
    if state:
        filter_dict["state"] = state
    if language:
        filter_dict["language"] = language
    if q:
        # simple text search on common fields
        filter_dict["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"title": {"$regex": q, "$options": "i"}},
            {"crop": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
        ]
    try:
        items = get_documents(name, filter_dict)
        # convert ObjectId to str for _id if present
        for it in items:
            if it.get("_id"):
                it["id"] = str(it.pop("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create endpoints
@app.post("/api/seeds")
def create_seed(seed: Seed):
    try:
        inserted_id = create_document("seed", seed)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/instruments")
def create_instrument(instrument: Instrument):
    try:
        inserted_id = create_document("instrument", instrument)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plants")
def create_plant(plant: Plant):
    try:
        inserted_id = create_document("plant", plant)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subsidies")
def create_subsidy(subsidy: Subsidy):
    try:
        inserted_id = create_document("subsidy", subsidy)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List endpoints with optional filters for state, language and query
@app.get("/api/seeds")
def list_seeds(state: Optional[str] = Query(None), language: Optional[str] = Query(None), q: Optional[str] = Query(None)):
    return _fetch_collection("seed", state, language, q)

@app.get("/api/instruments")
def list_instruments(state: Optional[str] = Query(None), language: Optional[str] = Query(None), q: Optional[str] = Query(None)):
    return _fetch_collection("instrument", state, language, q)

@app.get("/api/plants")
def list_plants(state: Optional[str] = Query(None), language: Optional[str] = Query(None), q: Optional[str] = Query(None)):
    return _fetch_collection("plant", state, language, q)

@app.get("/api/subsidies")
def list_subsidies(state: Optional[str] = Query(None), language: Optional[str] = Query(None), q: Optional[str] = Query(None)):
    return _fetch_collection("subsidy", state, language, q)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
