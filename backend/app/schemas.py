from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    timestamp: datetime
    vibration: float
    temperature: float
    pressure: float
    rpm: float
    device_id: str


class PredictionRequest(BaseModel):
    device_id: str
    readings: List[SensorReading]


class PredictionResponse(BaseModel):
    device_id: str
    failure_risk: float = Field(..., ge=0.0, le=1.0)
    horizon_hours: int
    model_version: str
    generated_at: datetime
    top_drivers: Optional[List[str]] = None


class DeviceSignalResponse(BaseModel):
    device_id: str
    status: str
    last_seen: datetime
    anomaly_score: float
