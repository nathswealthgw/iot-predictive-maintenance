from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas import DeviceSignalResponse, PredictionRequest, PredictionResponse
from app.services.prediction_client import TensorFlowServingClient

router = APIRouter()
client = TensorFlowServingClient()


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc)}


@router.post("/predict", response_model=PredictionResponse)
async def predict_failure(request: PredictionRequest) -> PredictionResponse:
    if not request.readings:
        raise HTTPException(status_code=400, detail="Readings cannot be empty")
    return await client.predict(request)


@router.get("/devices/{device_id}/signals", response_model=DeviceSignalResponse)
async def device_signals(device_id: str) -> DeviceSignalResponse:
    return DeviceSignalResponse(
        device_id=device_id,
        status="healthy",
        last_seen=datetime.now(timezone.utc),
        anomaly_score=0.08,
    )
