from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = Field("iot-predictive-maintenance-api", env="SERVICE_NAME")
    tf_serving_url: str = Field("http://tf-serving:8501", env="TF_SERVING_URL")
    model_name: str = Field("failure_predictor", env="MODEL_NAME")
    log_level: str = Field("INFO", env="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
