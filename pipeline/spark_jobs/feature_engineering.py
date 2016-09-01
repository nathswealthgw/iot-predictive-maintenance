from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg, stddev, max as spark_max


def build_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )


def main(raw_path: str, output_path: str) -> None:
    spark = build_spark("iot-feature-engineering")

    raw_df = spark.read.parquet(raw_path)
    windowed = (
        raw_df.withWatermark("timestamp", "10 minutes")
        .groupBy("device_id", window("timestamp", "5 minutes"))
        .agg(
            avg("vibration").alias("vibration_avg"),
            stddev("vibration").alias("vibration_std"),
            avg("temperature").alias("temperature_avg"),
            spark_max("temperature").alias("temperature_max"),
            avg("pressure").alias("pressure_avg"),
            avg("rpm").alias("rpm_avg"),
        )
        .withColumn("window_start", col("window.start"))
        .withColumn("window_end", col("window.end"))
        .drop("window")
    )

    windowed.write.mode("overwrite").parquet(output_path)
    spark.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, help="Raw telemetry parquet path")
    parser.add_argument("--output", required=True, help="Feature store output path")
    args = parser.parse_args()

    main(args.raw, args.output)
