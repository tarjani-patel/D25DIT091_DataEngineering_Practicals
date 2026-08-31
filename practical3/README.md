# Practical 3 — Data Ingestion Pipeline Comparison

## Objective

Design, implement and evaluate two parallel data ingestion pipelines:

- Periodic micro-batch ingestion
- Real-time event streaming

The pipelines are compared based on latency, throughput, scalability and fault tolerance.

## Technologies Used

- Python
- Redpanda
- Docker
- Kafka-Python-NG
- Pandas
- CSV
- PowerShell

## Project Structure

```text
practical3/
├── batch/
│   └── batch_pipeline.py
├── data/
├── metrics/
├── results/
├── streaming/
│   ├── producer.py
│   ├── consumer.py
│   ├── spike_producer.py
│   └── spike_consumer.py
├── tests/
├── docker-compose.yml
└── README.md


Experiments

1. Batch Ingestion

The batch pipeline processes user activity events in fixed-size batches.

Total events: 5,000
Batch size: 500
Batch interval: 5 seconds
Number of batches: 10
Metrics saved in: metrics/batch_metrics.csv

2. Real-Time Streaming

The streaming pipeline sends user activity events to the Redpanda user-activity topic.

Total events: 5,000
Topic: user-activity
Partitions: 3
Replicas: 3
Metrics saved in: metrics/streaming_metrics.csv

3. Traffic Spike and Consumer Scaling

A traffic spike was generated to test parallel consumer processing.

Total events: 15,000
Consumers: 3
Consumer group: spike-consumer-group

The events were distributed across the consumers:

Consumer 1: 4,972 events
Consumer 2: 4,994 events
Consumer 3: 5,034 events

4. Fault Tolerance

One Redpanda broker was stopped during the traffic-spike test.

Broker tested: redpanda-1
Events processed: 15,000
Events lost: 0
Average latency: 34.628 ms
Throughput: 137.87 events/sec
Metrics saved in: metrics/fault-consumer_spike_metrics.csv

Results
Test	            Events	Average Latency	 Throughput
Batch	            5,000	5001.39 ms	     99.97 events/sec
Normal Streaming	5,000	17.719 ms	     33.28 events/sec
3-Consumer Spike	15,000	22.635 ms	     —
Broker Failure	    15,000	34.628 ms	     137.87 events/sec

Key Observation

The batch pipeline provides a simple approach for processing data in groups but introduces higher latency due to periodic processing.

The streaming pipeline provides lower latency and supports parallel processing using multiple consumers. During the broker failure test, all 15,000 events were processed without data loss.

How to Run
1. Start Redpanda
docker compose up -d
2. Check Running Containers
docker ps
3. Create/Check the Topic
docker exec redpanda-0 rpk topic describe user-activity

The topic should have 3 partitions and 3 replicas.

Batch Pipeline

Run:

python batch\batch_pipeline.py

The batch metrics are saved to:

metrics/batch_metrics.csv


Normal Streaming

Start the consumer:

python streaming\consumer.py

Then run the producer in another terminal:

python streaming\producer.py

The metrics are saved to:

metrics/streaming_metrics.csv


Traffic Spike Test

Start Consumer 1:

$env:CONSUMER_ID="consumer-1"
python streaming\spike_consumer.py

Start Consumer 2 in another terminal:

$env:CONSUMER_ID="consumer-2"
python streaming\spike_consumer.py

Start Consumer 3 in another terminal:

$env:CONSUMER_ID="consumer-3"
python streaming\spike_consumer.py

Then run the spike producer:

python streaming\spike_producer.py

The consumers process the 15,000-event burst in parallel.

Fault-Tolerance Test

Stop one broker:

docker stop redpanda-1

Run the fault consumer:

$env:CONSUMER_ID="fault-consumer"
python streaming\spike_consumer.py

Generate the traffic spike:

python streaming\spike_producer.py

After the test, restart the broker:

docker start redpanda-1

Verify the topic again:

docker exec redpanda-0 rpk topic describe user-activity
Metrics

The metrics/ directory contains the performance data generated during the experiments:

batch_metrics.csv
streaming_metrics.csv
consumer-1_spike_metrics.csv
consumer-2_spike_metrics.csv
consumer-3_spike_metrics.csv
fault-consumer_spike_metrics.csv


Conclusion

The practical compares batch and real-time streaming ingestion under different workloads.

Batch ingestion is suitable for bulk processing where some delay is acceptable. Real-time streaming is more suitable for applications requiring continuous processing, lower latency and scalability through multiple consumers.

The fault-tolerance test also showed that the replicated Redpanda setup continued processing the workload when one broker was unavailable.