import os

from flask import Flask, request
from consumer import get_data, get_aggregated_data

app = Flask(__name__)


@app.route('/videos', methods=['GET'])
def get_trending():
    # Get query parameters from the request
    query_params = request.args

    # Filter based on query parameters
    videos = get_data(query_params)

    return videos


@app.route('/stats/<string:channel>', methods=['GET'])
def get_channel_stats(channel):
    stats = get_aggregated_data(channel)

    if stats:
        return stats
    else:
        return {"error": "Channel not found"}, 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
