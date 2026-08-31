import pandas as pd
import time
import os

INPUT_FILE = "data/user_activity.csv"
METRICS_FILE = "metrics/batch_metrics.csv"

BATCH_SIZE = 500
BATCH_INTERVAL = 5


def process_batch(batch):
    start_processing = time.perf_counter()

    # Simulate processing work
    total_events = len(batch)
    average_response = batch["response_time_ms"].mean()
    error_count = (batch["status_code"] >= 400).sum()

    processing_time = time.perf_counter() - start_processing

    return {
        "events": total_events,
        "average_response_ms": round(average_response, 2),
        "errors": int(error_count),
        "processing_time_ms": round(processing_time * 1000, 3)
    }


def main():

    df = pd.read_csv(INPUT_FILE)

    os.makedirs("metrics", exist_ok=True)

    metrics = []

    total_events = len(df)

    print("\n===== MICRO-BATCH PIPELINE =====")
    print(f"Total events: {total_events}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Batch interval: {BATCH_INTERVAL} seconds\n")

    batch_number = 1

    for start in range(0, total_events, BATCH_SIZE):

        batch = df.iloc[start:start + BATCH_SIZE]

        arrival_time = time.perf_counter()

        print(
            f"Batch {batch_number}: "
            f"{len(batch)} events received"
        )

        time.sleep(BATCH_INTERVAL)

        result = process_batch(batch)

        end_time = time.perf_counter()

        latency_ms = (end_time - arrival_time) * 1000

        throughput = (
            len(batch) / (end_time - arrival_time)
        )

        result["batch_number"] = batch_number
        result["latency_ms"] = round(latency_ms, 3)
        result["throughput_events_per_sec"] = round(
            throughput, 2
        )

        metrics.append(result)

        print(
            f"  Latency: {latency_ms:.2f} ms"
        )

        print(
            f"  Throughput: {throughput:.2f} events/sec"
        )

        batch_number += 1

    metrics_df = pd.DataFrame(metrics)

    metrics_df.to_csv(
        METRICS_FILE,
        index=False
    )

    print("\n===== BATCH PIPELINE COMPLETE =====")

    print(
        f"Average latency: "
        f"{metrics_df['latency_ms'].mean():.2f} ms"
    )

    print(
        f"Average throughput: "
        f"{metrics_df['throughput_events_per_sec'].mean():.2f} events/sec"
    )

    print(
        f"\nMetrics saved to: {METRICS_FILE}"
    )


if __name__ == "__main__":
    main()