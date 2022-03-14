import redis
import os
from models.user import User
from config import db as database


class Worker:

    def __init__(self):
        self._events = {}

    def listen(self, host, port, db):
        self._r = redis.Redis(host=host, port=port, db=db)
        stream = 'mystream'
        events = self._r.xread({stream: 0}, None, 0)[0][1]
        while True:
            event = self._r.xread({stream: "$"}, None, 0)
            if event[0][1] != events:
                event = User(name=event[0][1][-1])
                database.session.add(event)
                database.session.commit()
                events = event[0][1]


worker = Worker()
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')


if __name__ == "__main__":
    print("Hello world from worker.py")
    worker.listen(host=REDIS_HOST, port=6379, db=0)
