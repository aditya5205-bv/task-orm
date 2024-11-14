from logs.custom_logging import custom_logging
from redis import Redis
import json
from settings import REDIS_CONN
from datetime import date, datetime

class RedisConnection:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance
    
    def __init__(self, redis_config: dict):
        
        # self._host = None
        # self._port = None
        # self._decode_responses = None
        # self._redis = None
        self.is_initialized = False

    # def initialize(self, redis_config: dict):
        # if self.is_initialized:
        #     custom_logging.error("Connection is already initialized")
        #     return False
        
        try:
            self._host = redis_config.get('host')
            self._port = redis_config.get('port')
            self._decode_responses = redis_config.get('decode_responses')
                
            
            self._redis = Redis(host=self._host, port=self._port, decode_responses=self._decode_responses)
            
        except Exception as e:
            custom_logging.error(f"Error while connecting to redis {e}", exc_info=True)
            # trace_back = e.__traceback__
            # custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
    
    def disconnect(self):
        if self.is_initialized:
            self._redis.close()
            self._redis = None
            self.is_initialized = False
            
        custom_logging.info("Redis connection closed")
    
    
    def __enter__(self):
        self.initialize(REDIS_CONN)
        return self
    
    def __exit__(self):
        self.disconnect()
        
        
    def _json_serial(key, value):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(value, (datetime, date)):
            return value.strftime('%Y-%m-%d %H:%M:%S')
    
        raise TypeError("Type %s not serializable" % type(value))
    
        
    def set(self, key, data: dict, expire_in: int = 300):
        """Sets the dict in redis with default expiration of 5 min"""
        try:
            # serialize dict to string
            serialized_data = json.dumps(data, default=self._json_serial)
            

            self._redis.set(key, serialized_data)
            
            if expire_in != -1:
                self._redis.expire(key,expire_in)
                
            return True
        
        except Exception as e:
            custom_logging.error(f"Redis set error: {e}", exc_info=True)
            
        
    def get(self, key):
        """Gets the dict from redis using key"""
        try:
            
            data = self._redis.get(key)
            
            if data == None:
                custom_logging.warning("====Cache miss====")
                return False
            else:
                custom_logging.info("====Cache hit====")
            
            # convert string data to dict
            data = json.loads(data)
                
            return data
            
        except Exception as e:
            custom_logging.error(f"Redis get error {e}", exc_info=True)

