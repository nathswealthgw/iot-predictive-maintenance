from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean, stdev
from typing import List

import httpx

from app.config import get_settings
from app.schemas import PredictionRequest, PredictionResponse


class TensorFlowServingClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.tf_serving_url.rstrip("/")
        self.model_name = settings.model_name

    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        payload = self._build_payload(request.readings)
        url = f"{self.base_url}/v1/models/{self.model_name}:predict"
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        score = float(data["predictions"][0][0])
        return PredictionResponse(
            device_id=request.device_id,
            failure_risk=score,
            horizon_hours=72,
            model_version=data.get("model_version", "unknown"),
            generated_at=datetime.now(timezone.utc),
            top_drivers=["vibration", "temperature"],
        )

    @staticmethod
    def _build_payload(readings: List) -> dict:
        vibration_values = [reading.vibration for reading in readings]
        temperature_values = [reading.temperature for reading in readings]
        pressure_values = [reading.pressure for reading in readings]
        rpm_values = [reading.rpm for reading in readings]

        vibration_std = stdev(vibration_values) if len(vibration_values) > 1 else 0.0

        engineered_features = [
            mean(vibration_values),
            vibration_std,
            mean(temperature_values),
            max(temperature_values),
            mean(pressure_values),
            mean(rpm_values),
        ]
        return {"instances": [engineered_features]}
