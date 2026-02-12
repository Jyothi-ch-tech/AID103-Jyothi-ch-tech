from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import FarmData
from ai_engine import analyze_crop
from advisory import generate_advisory
from alerts import generate_alert

class AnalyzeRequest(BaseModel):
    image_path: str
    farm_data: FarmData

app = FastAPI(title="CropGuard AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    analysis = analyze_crop(request.image_path, request.farm_data.dict())
    advisory = generate_advisory(analysis["disease"], analysis["severity"])
    alert = generate_alert(analysis["severity"])

    return {
        "AI_Analysis": analysis,
        "Advisory": advisory,
        "Alert": alert
    }
