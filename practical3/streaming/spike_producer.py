import csv
import json
import time

from kafka import KafkaProducer

BOOTSTRAP_SERVERS = ["localhost:19092"]
TOPIC = "user-activity"
INPUT_FILE = "data/user_activity.csv"

REPEAT_COUNT = 3


def create_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        acks="all",
        retries=5,
        linger_ms=0
    )


def main():

    producer = create_producer()

    print("\n===== TRAFFIC SPIKE PRODUCER =====")
    print(f"Topic: {TOPIC}")
    print(f"Rounds: {REPEAT_COUNT}")
    print("Sending events as a burst...\n")

    sent_count = 0

    with open(INPUT_FILE, "r", newline="") as file:

        rows = list(csv.DictReader(file))

    start_time = time.perf_counter()

    for round_number in range(1, REPEAT_COUNT + 1):

        for row in rows:

            event = dict(row)

            event["producer_timestamp"] = time.time()
            event["spike_round"] = round_number

            producer.send(
                TOPIC,
                value=event
            )

            sent_count += 1

            if sent_count % 1000 == 0:
                print(f"Sent {sent_count} events")

    producer.flush()
    producer.close()

    elapsed = time.perf_counter() - start_time

    print("\n===== SPIKE PRODUCER COMPLETE =====")
    print(f"Total events sent: {sent_count}")
    print(f"Send time: {elapsed:.3f} seconds")
    print(
        f"Producer rate: "
        f"{sent_count / elapsed:.2f} events/sec"
    )


if __name__ == "__main__":
    main()