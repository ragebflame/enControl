import os
import redis
from rq import Worker, Queue, Connection

# Assign the needed variables
listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

# start the Worker
with Connection(conn):
    worker = Worker(list(map(Queue, listen)))
    worker.work()

