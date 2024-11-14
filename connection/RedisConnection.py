from connection.Connection import SingletonMeta
from logs.custom_logging import custom_logging
from redis import Redis

class RedisConnection(metaclass=SingletonMeta):
    
    def __init__(self, redis_config: dict):
        
        self._host = redis_config.get('host')
        self._port = redis_config.get('port')
        self._decode_responses = redis_config.get('decode_responses')
        
        self._redis = None
        self.is_initialized = False

    def initialize(self):
        if self.is_initialized:
            custom_logging.error("Connection is already initialized")
            return False
        
        try:
            self._redis = Redis(host=self._host, port=self._port, decode_responses=self._decode_responses)
            
        except Exception as e:
            custom_logging.error(f"Error while connecting to redis: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
    
    def disconnect(self):
        if self.is_initialized:
            self._redis.close()
            self._redis = None
            self.is_initialized = False
            
        custom_logging.info("Redis connection closed")
    
    def get_redis(self):
        return self._redis
    
    def __enter__(self):
        self.initialize()
        return self._redis
    
    def __exit__(self):
        self.disconnect()