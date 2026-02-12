from pydantic import BaseModel

class FarmData(BaseModel):
    crop: str
    location: str
    growth_stage: str
