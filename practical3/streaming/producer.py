import csv
import json
import time
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = ["localhost:19092"]
TOPIC = "user-activity"
INPUT_FILE = "data/user_activity.csv"


def create_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        acks="all",
        retries=5,
        linger_ms=5
    )


def main():

    producer = create_producer()

    print("\n===== STREAMING PRODUCER =====")
    print(f"Topic: {TOPIC}")
    print("Connecting to Redpanda...")

    sent_count = 0

    with open(INPUT_FILE, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            row["producer_timestamp"] = time.time()

            producer.send(
                TOPIC,
                value=row
            )

            sent_count += 1

            if sent_count % 500 == 0:
                producer.flush()
                print(f"Sent {sent_count} events")

    producer.flush()
    producer.close()

    print("\n===== PRODUCER COMPLETE =====")
    print(f"Total events sent: {sent_count}")


if __name__ == "__main__":
    main()