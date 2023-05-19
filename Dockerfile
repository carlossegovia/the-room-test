FROM python:3.8.10

WORKDIR /app

# Copy requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all the scripts and apps to the container
COPY dataset /app/dataset
COPY streaming_simulator.py /app/streaming_simulator.py
COPY app.py /app/app.py
COPY consumer.py /app/consumer.py

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
