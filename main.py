import os
import time

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

# Elasticsearch connection
es = Elasticsearch(hosts=['http://localhost:9200'])

# Directory path containing the CSV files
directory_path = './dataset/'
index_name = 'trending_youtube_video_statistics'
unique_field = 'video_id'

mapping = {
    "mappings": {
        "properties": {
            unique_field: {
                "type": "keyword"
            },
            "trending_date": {
                "type": "text"
            },
            "title": {
                "type": "text"
            },
            "channel_title": {
                "type": "keyword"
            },
            "category_id": {
                "type": "long"
            },
            "publish_time": {
                "type": "date"
            },
            "tags": {
                "type": "text"
            },
            "views": {
                "type": "long"
            },
            "likes": {
                "type": "long"
            },
            "dislikes": {
                "type": "long"
            },
            "comment_count": {
                "type": "long"
            },
            "thumbnail_link": {
                "type": "text"
            },
            "comments_disabled": {
                "type": "boolean"
            },
            "ratings_disabled": {
                "type": "boolean"
            },
            "video_error_or_removed": {
                "type": "boolean"
            },
            "description": {
                "type": "text"
            }
        }
    }
}

schema = {
    "video_id": str,
    "trending_date": str,
    "title": str,
    "channel_title": str,
    "category_id": int,
    "publish_time": str,
    "tags": str,
    "views": int,
    "likes": int,
    "dislikes": int,
    "comment_count": int,
    "thumbnail_link": str,
    "comments_disabled": bool,
    "ratings_disabled": bool,
    "video_error_or_removed": bool,
    "description": str
}

string_columns = ["video_id", "trending_date", "title", "channel_title", "publish_time", "tags", "thumbnail_link",
                  "description"]


def create_index(index_name):
    # Create the index if it doesn't exist
    try:
        es.indices.create(index=index_name, body=mapping)
    except RequestError as e:
        if e.error == 'resource_already_exists_exception':
            print(f"Index '{index_name}' already exists.")
        else:
            raise e


def simulate_streaming_pandas(interval):
    # Iterate over each CSV file
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path, dtype=schema, encoding='latin1')

            df[string_columns] = df[string_columns].astype(str)

            # Convert DataFrame records to JSON format
            records = df.to_dict(orient='records')

            # Send records to Elasticsearch
            for record in records:
                # Index each record in Elasticsearch
                print(record, type(record['description']))
                es.index(index=index_name, id=record[unique_field], document=record)
                # Wait for a few seconds before send the next record
                time.sleep(interval)


if __name__ == '__main__':
    create_index(index_name)
    simulate_streaming_pandas(0)
