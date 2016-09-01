import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from pyspark.sql import SparkSession

FEATURE_COLUMNS = [
    "vibration_avg",
    "vibration_std",
    "temperature_avg",
    "temperature_max",
    "pressure_avg",
    "rpm_avg",
]


def build_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def load_training_data(spark: SparkSession, path: str) -> tuple[np.ndarray, np.ndarray]:
    df = spark.read.parquet(path).dropna(subset=FEATURE_COLUMNS + ["failure"])
    pandas_df = df.select(FEATURE_COLUMNS + ["failure"]).toPandas()

    features = pandas_df[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
    labels = pandas_df["failure"].to_numpy(dtype=np.float32)
    return features, labels


def build_model(input_dim: int) -> tf.keras.Model:
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(input_dim,)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["AUC"])
    return model


def main(features_path: str, model_dir: str) -> None:
    spark = build_spark("iot-model-training")
    features, labels = load_training_data(spark, features_path)

    model = build_model(features.shape[1])
    model.fit(features, labels, epochs=8, batch_size=256, validation_split=0.2)

    export_path = Path(model_dir) / "1"
    export_path.mkdir(parents=True, exist_ok=True)
    model.save(export_path)

    spark.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--features", required=True, help="Path to feature store")
    parser.add_argument("--model-dir", required=True, help="TF Serving model dir")
    args = parser.parse_args()

    main(args.features, args.model_dir)
