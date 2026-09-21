import subprocess
import re
import pandas as pd
import time

RUNS = 3

etl_results = []
elt_results = []

print("=" * 70)
print("ETL vs ELT PERFORMANCE BENCHMARK")
print("=" * 70)

# ---------------------------------------------------------
# RUN ETL PIPELINE
# ---------------------------------------------------------
print("\nRunning ETL pipeline...")

for run in range(1, RUNS + 1):

    print(f"ETL Run {run}/{RUNS}")

    start = time.perf_counter()

    result = subprocess.run(
        ["python", "etl_pipeline.py"],
        capture_output=True,
        text=True
    )

    elapsed = time.perf_counter() - start

    output = result.stdout

    match = re.search(
        r"Total ETL time\s*:\s*([0-9.]+)",
        output
    )

    if match:
        pipeline_time = float(match.group(1))
    else:
        pipeline_time = elapsed

    etl_results.append(pipeline_time)

    if result.returncode != 0:
        print("ETL pipeline failed!")
        print(result.stderr)


# ---------------------------------------------------------
# RUN ELT PIPELINE
# ---------------------------------------------------------
print("\nRunning ELT pipeline...")

for run in range(1, RUNS + 1):

    print(f"ELT Run {run}/{RUNS}")

    start = time.perf_counter()

    result = subprocess.run(
        ["python", "elt_pipeline.py"],
        capture_output=True,
        text=True
    )

    elapsed = time.perf_counter() - start

    output = result.stdout

    match = re.search(
        r"Total ELT time\s*:\s*([0-9.]+)",
        output
    )

    if match:
        pipeline_time = float(match.group(1))
    else:
        pipeline_time = elapsed

    elt_results.append(pipeline_time)

    if result.returncode != 0:
        print("ELT pipeline failed!")
        print(result.stderr)


# ---------------------------------------------------------
# CALCULATE AVERAGES
# ---------------------------------------------------------
etl_average = sum(etl_results) / len(etl_results)
elt_average = sum(elt_results) / len(elt_results)

difference = etl_average - elt_average

if etl_average != 0:
    percentage_difference = (difference / etl_average) * 100
else:
    percentage_difference = 0


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------
print("\n" + "=" * 70)
print("PERFORMANCE RESULTS")
print("=" * 70)

print("\nETL Times:")
for i, value in enumerate(etl_results, 1):
    print(f"Run {i}: {value:.4f} seconds")

print(f"ETL Average: {etl_average:.4f} seconds")

print("\nELT Times:")
for i, value in enumerate(elt_results, 1):
    print(f"Run {i}: {value:.4f} seconds")

print(f"ELT Average: {elt_average:.4f} seconds")

print("\n" + "-" * 70)
print("COMPARISON")
print("-" * 70)

print(f"Average ETL time : {etl_average:.4f} seconds")
print(f"Average ELT time : {elt_average:.4f} seconds")
print(f"Difference       : {abs(difference):.4f} seconds")
print(f"Difference (%)   : {abs(percentage_difference):.2f}%")


# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------
results_df = pd.DataFrame({
    "Pipeline": ["ETL", "ELT"],
    "Run_1_seconds": [etl_results[0], elt_results[0]],
    "Run_2_seconds": [etl_results[1], elt_results[1]],
    "Run_3_seconds": [etl_results[2], elt_results[2]],
    "Average_seconds": [etl_average, elt_average]
})

results_df.to_csv(
    "output/performance_results.csv",
    index=False
)

print("\nPerformance results saved to:")
print("output/performance_results.csv")

print("\n" + "=" * 70)
print("BENCHMARK COMPLETED SUCCESSFULLY!")
print("=" * 70)