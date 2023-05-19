from elasticsearch import Elasticsearch
import pandas as pd

es = Elasticsearch(hosts=['http://localhost:9200'])

index_name = 'trending_youtube_video_statistics'


def format_query(raw_query):
    pairs = raw_query.split(";")
    data = {}

    # Iterate over each pair and split it by '='
    for pair in pairs:
        # Split the pair into field and value
        parts = pair.split("=")
        if len(parts) == 2:
            # Assign the field and value to the dictionary
            field = parts[0]
            value = parts[1]
            data[field] = value
        else:
            # Show an error if the format is not correct
            raise ValueError("Invalid format: {}".format(raw_query))
    return data


def get_data(query):
    bool_query = {
        'query': {
            'bool': {
                'must': [{'match': {field: value}} for field, value in format_query(query).items()]
            }
        }
    }

    response = es.search(index=index_name, body=bool_query, size=10000)
    hits = response['hits']['hits']
    df = pd.DataFrame([hit['_source'] for hit in hits])
    return df.to_json(orient='records')


def get_aggregated_data(channel_title):
    # Define the aggregation query with a filter on channel_title
    aggregation_query = {
        "size": "0",
        "aggs": {
            "channel_title_stats": {
                "filter": {"term": {"channel_title": channel_title}},
                "aggs": {
                    "avg_likes": {"avg": {"field": "likes"}},
                    "sum_likes": {"sum": {"field": "likes"}},
                    "avg_views": {"avg": {"field": "views"}},
                    "sum_views": {"sum": {"field": "views"}},
                    "avg_dislikes": {"avg": {"field": "dislikes"}},
                    "sum_dislikes": {"sum": {"field": "dislikes"}},
                    "avg_comment_count": {"avg": {"field": "comment_count"}},
                    "sum_comment_count": {"sum": {"field": "comment_count"}}
                }
            }
        }
    }

    # Execute the search query with aggregation
    response = es.search(index=index_name, body=aggregation_query)

    # Access the aggregation results
    bucket = response['aggregations']['channel_title_stats']

    # Process the bucket for the specified channel_title
    stats = {}
    if bucket:
        stats["channel_title"] = channel_title
        for k, v in bucket.items():
            if k == 'doc_count':
                stats['total_videos'] = v
            else:
                stats[k] = v['value']
    return stats


if __name__ == '__main__':
    # result = get_data("channel_title=Albert Plash")
    # print(result)
    print(get_aggregated_data("Vat19"))
