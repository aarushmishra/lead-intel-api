"""
FastAPI application for lead enrichment microservice.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
from .runtime import enrich_lead

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lead Intelligence API",
    description="AI dialer lead enrichment microservice",
    version="1.0.0"
)

class LeadRequest(BaseModel):
    college: Optional[str] = Field(default="", description="College name (optional)")
    city: Optional[str] = Field(default="", description="City name (optional)")
    state: str = Field(..., description="State name (required)")
    course: str = Field(..., description="Course name")
    language: Optional[str] = Field(default="", description="Preferred language (optional)")

class LeadResponse(BaseModel):
    college: Optional[str]
    city: Optional[str]
    state: str
    course: str
    language: Optional[str]
    caller_name: str
    pitch_text: str
    tts_languages: List[str]

@app.get("/")
def read_root():
    return {"message": "Lead Intelligence API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "lead-intel-api"}

@app.post("/enrich_lead", response_model=LeadResponse)
def enrich_lead_endpoint(lead: LeadRequest):
    try:
        lead_dict = lead.model_dump()
        enriched_lead = enrich_lead(lead_dict)
        logger.info(f"Successfully enriched lead for state: {lead.state}")
        return LeadResponse(**enriched_lead)
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Internal error: {str(e)}")
        raise HTTPException(status_code=500, detail="internal_error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
