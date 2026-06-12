# DADS6005 Data Streaming with Kafka + KsqlDB

โปรเจกต์ Data Streaming สำหรับรายวิชา DADS6005 (Quiz 2) 
ใช้ **Apache Kafka**, **Debezium CDC**, และ **KsqlDB** 
เพื่อทำ Real-time Stream Processing กับชุดข้อมูล Food Survey (food_coded.csv)

## Architecture

```
PostgreSQL (Source)
    │
    ▼  (Debezium CDC)
Kafka Topic: source.public.db_food_coded2_stream
    │
    ├──▶ Kafka Consumer (Python)
    │
    ├──▶ KsqlDB Stream Processing
    │       ├── food_coded_stream (raw AVRO)
    │       ├── food_flat_stream (flat JSON)
    │       ├── avg_calories_by_gender (TABLE)
    │       ├── exercise_vs_diet (TABLE)
    │       ├── comfort_food_reasons_stats (TABLE)
    │       ├── nutrition_by_income (TABLE)
    │       └── top_cuisines (TABLE)
    │
    └──▶ Dash Dashboard (Visualization)
```

## Services (Docker)

| Service | Port | Description |
|---------|------|-------------|
| Zookeeper | 2181 | Coordination |
| Kafka | 29092 | Message broker |
| Schema Registry | 8081 | Schema management |
| Debezium Connect | 8083 | CDC connector |
| Kafka Manager | 9000 | Kafka UI |
| **KsqlDB Server** | **8088** | **Stream processing engine** |
| **KsqlDB CLI** | - | **Interactive SQL CLI** |

## Quick Start

### 1. Start Docker services
```bash
docker-compose up -d
```

### 2. Configure Debezium connector (via REST API)
```bash
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
  "name": "food-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "123456",
    "database.dbname": "dbfood",
    "database.server.name": "source",
    "table.include.list": "public.db_food_coded2_stream",
    "plugin.name": "pgoutput"
  }
}'
```

### 3. Run KsqlDB setup
```bash
# Interactive CLI
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

# Or run script files via REST
python pipeline.py ksql --script ksqldb/01_create_streams.ksql
python pipeline.py ksql --script ksqldb/02_create_tables.ksql
```

### 4. Stream data to Kafka
```bash
python pipeline.py stream --csv food_coded.csv --topic food_coded_json --interval 1
```

### 5. Run analytics queries
```bash
python pipeline.py ksql --script ksqldb/03_analytics_queries.ksql
```

### 6. List Kafka topics
```bash
python pipeline.py list-topics
```

## KsqlDB Scripts

| File | Description |
|------|-------------|
| `ksqldb/01_create_streams.ksql` | สร้าง STREAM จาก Debezium CDC topic |
| `ksqldb/02_create_tables.ksql` | สร้าง Materialized Tables สำหรับ aggregation |
| `ksqldb/03_analytics_queries.ksql` | Push & Pull queries สำหรับวิเคราะห์ข้อมูล |

## Interesting Insights from Data

1. **Comfort Food & Stress Correlation** — วิเคราะห์ความสัมพันธ์ระหว่าง comfort food reasons กับ GPA
2. **Gender & Calorie Patterns** — เปรียบเทียบ calories ระหว่างเพศ
3. **Exercise vs Diet Quality** — คนออกกำลังกายมากกินสุขภาพดีกว่าจริงหรือ?
4. **Income & Nutrition** — รายได้สูงกินผักผลไม้มากกว่าไหม?
5. **Favorite Cuisines** — Top cuisines แบบ real-time

## Files

| File | Description |
|------|-------------|
| `docker-compose.yml` | Docker services configuration |
| `food_coded.csv` | Food survey dataset (125 records) |
| `pipeline.py` | Python CLI for streaming + KsqlDB |
| `Kafka Producer.ipynb` | Basic producer notebook |
| `Kafka Consumer.ipynb` | Basic consumer notebook |
| `Insert_records_connect.ipynb` | CDC insert + Dash dashboard |
| `List topics and read sales Data Stream.ipynb` | Topic listing + Debezium consumer |
| `ksqldb/` | KsqlDB SQL scripts |
| `requirements.txt` | Python dependencies |
