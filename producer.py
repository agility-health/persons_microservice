import functools
import redis


class Producer:

    def __init__(self, stream_name, host, port, db):
        self.stream = stream_name
        self._r = redis.Redis(host=host, port=port, db=db)

    def event(self, action, data={}):
        def decorator(func):
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                result = func(*args, **kwargs)
                arg_keys = func.__code__.co_varnames[1:-1]
                for i in range(1, len(args)):
                    kwargs[arg_keys[i-1]] = args[i]
                body = {
                    "action": action
                }
                for k, v in data.items():
                    body[k] = v
                self._r.xadd(self.stream, body)
                return result
            return wrapped
        return decorator
