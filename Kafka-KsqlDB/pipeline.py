"""
Data Streaming Pipeline with Kafka + KsqlDB
DADS6005 Data Streaming - Quiz 2 (KsqlDB)
"""

import json
import csv
import time
import argparse
import requests
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

KAFKA_BROKER = 'localhost:29092'
KSQLDB_URL = 'http://localhost:8088'


def create_topic(topic_name, partitions=1, replication=1):
    admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
    try:
        topic_list = [NewTopic(name=topic_name, num_partitions=partitions, replication_factor=replication)]
        admin.create_topics(new_topics=topic_list, validate_only=False)
        print(f"[OK] Topic '{topic_name}' created")
    except Exception as e:
        print(f"[!] Topic '{topic_name}' might already exist: {e}")


def stream_csv_to_kafka(csv_path, topic, interval=1.0, max_rows=None):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if max_rows and i >= max_rows:
                break
            producer.send(topic, value=row)
            print(f"[{i+1}] Sent user_id={row.get('ids','?')} -> '{topic}'")
            time.sleep(interval)
    producer.flush()
    print(f"[Done] Streamed {i+1} records to '{topic}'")


def ksqldb_query(sql):
    payload = {"ksql": sql, "streamsProperties": {}}
    resp = requests.post(f"{KSQLDB_URL}/ksql", json=payload)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"[ERROR] KsqlDB: {resp.status_code} - {resp.text}")
        return None


def ksqldb_query_streaming(sql, callback=None):
    payload = {"sql": sql, "streamsProperties": {}}
    resp = requests.post(f"{KSQLDB_URL}/query", json=payload, stream=True)
    if resp.status_code != 200:
        print(f"[ERROR] KsqlDB stream: {resp.status_code}")
        return
    for line in resp.iter_lines():
        if line:
            try:
                data = json.loads(line.decode('utf-8'))
                if callback:
                    callback(data)
                else:
                    print(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                continue


def run_ksqldb_script(script_path):
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    statements = [s.strip() for s in content.split(';') if s.strip() and not s.strip().startswith('--')]
    for stmt in statements:
        if stmt.upper().startswith('SELECT') and 'EMIT CHANGES' not in stmt.upper():
            print(f"\n[PULL QUERY] {stmt[:60]}...")
            result = ksqldb_query(stmt)
            if result:
                for row in result[0].get('rows', []):
                    print(row)
        elif 'EMIT CHANGES' in stmt.upper():
            print(f"\n[PUSH QUERY] {stmt[:60]}...")
        else:
            print(f"\n[EXEC] {stmt[:60]}...")
            ksqldb_query(stmt)
            time.sleep(0.5)


def list_topics():
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_BROKER)
    topics = consumer.topics()
    print("Kafka Topics:")
    for t in sorted(topics):
        print(f"  - {t}")
    return topics


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Food Survey Data Streaming Pipeline')
    parser.add_argument('action', choices=['list-topics', 'stream', 'ksql', 'all'],
                        help='Action to perform')
    parser.add_argument('--csv', default='food_coded.csv', help='Path to CSV file')
    parser.add_argument('--topic', default='food_coded_json', help='Kafka topic name')
    parser.add_argument('--interval', type=float, default=1.0, help='Stream interval (seconds)')
    parser.add_argument('--max-rows', type=int, default=None, help='Max rows to stream')
    parser.add_argument('--script', default='ksqldb/01_create_streams.ksql',
                        help='KsqlDB script path')
    args = parser.parse_args()

    if args.action == 'list-topics':
        list_topics()

    elif args.action == 'stream':
        create_topic(args.topic)
        stream_csv_to_kafka(args.csv, args.topic, args.interval, args.max_rows)

    elif args.action == 'ksql':
        run_ksqldb_script(args.script)

    elif args.action == 'all':
        print("=" * 60)
        print("  Food Survey Data Streaming Pipeline")
        print("=" * 60)

        create_topic(args.topic)

        print("\n>>> Running KsqlDB setup...")
        for script in ['ksqldb/01_create_streams.ksql',
                       'ksqldb/02_create_tables.ksql']:
            run_ksqldb_script(script)

        print("\n>>> Streaming data to Kafka...")
        stream_csv_to_kafka(args.csv, args.topic, args.interval, args.max_rows)

        print("\n>>> Running analytics queries...")
        run_ksqldb_script('ksqldb/03_analytics_queries.ksql')

        print("\n" + "=" * 60)
        print("  Pipeline completed!")
        print("=" * 60)
