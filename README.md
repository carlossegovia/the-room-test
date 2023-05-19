# The-room-challenge

Principal Data Engineer - Assignment

## Description

This is a coding task. Python is preferred, but use any language you are comfortable with.
- Download the Trending YouTube Video Statistics dataset from Kaggle
- Create a streaming process that simulates each record in this dataset appearing
sequentially in a (user configurable) time-delayed manner 
- Each record needs to sent to some datastore (your choice of Sql, Nosql) and be
searchable, in real time, by any attribute 
- Generate in real time, aggregate statistics by the channel_title attribute
- Write API endpoints to query for individual records by one or more attributes aggregate statistics by channel
- Extra credit: Containerize streaming data generator, datastore, query layer

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/carlossegovia/the-room-test.git
   ```

2. Change to the project directory:

   ```bash
   cd the-room-test
   ```

3. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Containers

To start the project's containers, run the following command:

```bash
docker-compose up -d
```

This will start the Elasticsearch, Kibana, and Flask app containers defined in the `docker-compose.yaml` file.

### Streaming Data to Elasticsearch

To simulate streaming data from CSV files to Elasticsearch, run the following command:

```bash
docker exec -it <container_id_or_name> python /app/streaming_simulator.py <interval>
```
Replace `<container_id_or_name>` with `the-room-test-flask_app-1`
Replace `<interval>` with the desired interval in seconds between each record. This script will read data from CSV files located in the `dataset` directory and write them to Elasticsearch.

Example: 
```bash
docker exec -it the-room-test-flask_app-1 python /app/streaming_simulator.py 5
```

### Accessing the Endpoints

Once the containers are up and running, you can access the following endpoints to query the data:

- **GET /videos**: Get trending videos.

Examples:

```bash
curl http://localhost:5000/videos?param1=value1&param2=value2

# Search by only one field
curl http://localhost:5000/videos?video_id=gUkB5Kk4WAA

# Search by multiples fields
curl http://localhost:5000/videos\?trending_date\=17.27.11\&description\=for%20the
```


- **GET /stats/{channel}**: Get aggregated statistics for a specific channel.

Example:

```bash
curl http://localhost:5000/stats/channel-name

curl http://localhost:5000/stats/Luisito%20Comunica
```

Replace `channel-name` with the desired channel name.

