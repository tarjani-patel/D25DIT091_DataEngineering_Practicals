import json
import os
import time

import pandas as pd
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = ["localhost:19092"]
TOPIC = "user-activity"
GROUP_ID = "spike-consumer-group"

IDLE_TIMEOUT = 5

CONSUMER_ID = os.environ.get(
    "CONSUMER_ID",
    "consumer-1"
)

METRICS_FILE = (
    f"metrics/{CONSUMER_ID}_spike_metrics.csv"
)


def create_consumer():

    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda value:
            json.loads(value.decode("utf-8"))
    )


def main():

    consumer = create_consumer()

    print("\n===== SPIKE CONSUMER =====")
    print(f"Consumer ID: {CONSUMER_ID}")
    print(f"Consumer group: {GROUP_ID}")
    print(f"Idle timeout: {IDLE_TIMEOUT} seconds")
    print("Waiting for traffic...\n")

    results = []

    processed = 0
    start_time = time.perf_counter()
    last_message_time = time.perf_counter()

    try:

        while True:

            records = consumer.poll(
                timeout_ms=1000
            )

            if records:

                last_message_time = time.perf_counter()

                for topic_partition, messages in records.items():

                    for message in messages:

                        consumer_timestamp = time.time()

                        event = message.value

                        producer_timestamp = event.get(
                            "producer_timestamp"
                        )

                        if producer_timestamp is not None:

                            latency_ms = (
                                consumer_timestamp
                                - producer_timestamp
                            ) * 1000

                        else:

                            latency_ms = 0

                        results.append({
                            "consumer_id": CONSUMER_ID,
                            "event_id": event["event_id"],
                            "partition": message.partition,
                            "offset": message.offset,
                            "latency_ms": round(
                                latency_ms, 3
                            )
                        })

                        processed += 1

            else:

                idle_time = (
                    time.perf_counter()
                    - last_message_time
                )

                if processed > 0 and idle_time >= IDLE_TIMEOUT:
                    break

    finally:

        consumer.close()

    elapsed = time.perf_counter() - start_time

    if results:

        metrics_df = pd.DataFrame(results)

        metrics_df.to_csv(
            METRICS_FILE,
            index=False
        )

        average_latency = (
            metrics_df["latency_ms"].mean()
        )

    else:

        average_latency = 0

    throughput = (
        processed / elapsed
        if elapsed > 0
        else 0
    )

    print("\n===== SPIKE CONSUMER COMPLETE =====")

    print(f"Consumer ID: {CONSUMER_ID}")
    print(f"Events processed: {processed}")
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