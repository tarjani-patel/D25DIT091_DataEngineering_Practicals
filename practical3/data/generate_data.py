import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "data/user_activity.csv"
TOTAL_EVENTS = 5000

event_types = [
    "page_view",
    "login",
    "logout",
    "click",
    "search",
    "add_to_cart",
    "purchase"
]

pages = [
    "/",
    "/home",
    "/products",
    "/product/101",
    "/product/102",
    "/search",
    "/cart",
    "/checkout",
    "/profile",
    "/login"
]

servers = [
    "server-1",
    "server-2",
    "server-3"
]

status_codes = [200, 200, 200, 200, 201, 400, 404, 500]

start_time = datetime.now()

with open(OUTPUT_FILE, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "event_id",
        "user_id",
        "event_type",
        "page",
        "event_timestamp",
        "server",
        "response_time_ms",
        "status_code"
    ])

    for i in range(1, TOTAL_EVENTS + 1):
        event_time = start_time + timedelta(
            milliseconds=i * 10
        )

        writer.writerow([
            i,
            f"U{random.randint(1, 1000):04d}",
            random.choice(event_types),
            random.choice(pages),
            event_time.isoformat(timespec="milliseconds"),
            random.choice(servers),
            random.randint(40, 800),
            random.choice(status_codes)
        ])

print(f"Generated {TOTAL_EVENTS} events.")
print(f"Saved dataset to: {OUTPUT_FILE}")