import json
import os
import time

import pandas as pd
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ["localhost:19092"]
TOPIC = "user-activity"
GROUP_ID = "streaming-consumer-group"

METRICS_FILE = "metrics/streaming_metrics.csv"

TARGET_EVENTS = 5000


def create_consumer():

    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        )
    )


def main():

    os.makedirs("metrics", exist_ok=True)

    consumer = create_consumer()

    print("\n===== STREAMING CONSUMER =====")
    print(f"Topic: {TOPIC}")
    print(f"Consumer group: {GROUP_ID}")
    print(f"Target events: {TARGET_EVENTS}\n")

    results = []

    processed = 0
    start_time = time.perf_counter()

    try:

        for message in consumer:

            process_start = time.time()

            event = message.value

            producer_timestamp = event.get(
                "producer_timestamp"
            )

            if producer_timestamp is not None:

                latency_ms = (
                    process_start - producer_timestamp
                ) * 1000

            else:

                latency_ms = 0

            results.append({
                "event_id": event["event_id"],
                "partition": message.partition,
                "offset": message.offset,
                "latency_ms": round(latency_ms, 3),
                "status_code": event["status_code"],
                "response_time_ms": event[
                    "response_time_ms"
                ]
            })

            processed += 1

            if processed % 500 == 0:

                elapsed = (
                    time.perf_counter() - start_time
                )

                throughput = processed / elapsed

                print(
                    f"Processed {processed} events | "
                    f"Throughput: "
                    f"{throughput:.2f} events/sec"
                )

            if processed >= TARGET_EVENTS:
                break

    finally:

        consumer.close()

    metrics_df = pd.DataFrame(results)

    metrics_df.to_csv(
        METRICS_FILE,
        index=False
    )

    total_time = (
        time.perf_counter() - start_time
    )

    average_latency = (
        metrics_df["latency_ms"].mean()
    )

    throughput = processed / total_time

    print("\n===== STREAMING CONSUMER COMPLETE =====")

    print(
        f"Events processed: {processed}"
    )

    print(
        f"Average latency: "
        f"{average_latency:.3f} ms"
    )

    print(
        f"Throughput: "
        f"{throughput:.2f} events/sec"
    )

    print(
        f"Metrics saved to: {METRICS_FILE}"
    )


if __name__ == "__main__":
    main()