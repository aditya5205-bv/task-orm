import json
from redis import Redis
from connection.Connection import SingletonMeta
from logs.custom_logging import custom_logging
from datetime import date, datetime

class RedisCache(metaclass=SingletonMeta):
    
    def __init__(self, redis_config: dict):
        
        self._host = redis_config.get('host')
        self._port = redis_config.get('port')
        self._decode_responses = redis_config.get('decode_responses')
        
        self._redis = None
        self._redis = Redis(host=self._host, port=self._port, decode_responses=self._decode_responses)
        
        
    def _json_serial(key, value):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(value, (datetime, date)):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError ("Type %s not serializable" % type(value))
    
        
    def set(self, key, data: dict, expire_in: int = 300):
        """Sets the dict in redis with default expiration of 5 min"""
        try:
            # serialize dict to string
            serialized_data = json.dumps(data, default=self._json_serial)
            
            if not self._redis:
                custom_logging.error("Redis not initalized")
                return False

            res = self._redis.set(key, serialized_data)
            
            if expire_in != -1:
                self._redis.expire(key,expire_in)
                
            return True
        
        except Exception as e:
            custom_logging.error(f"Redis set error: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
        
    def get(self, key):
        """Gets the dict from redis using key"""
        try:
            if not self._redis:
                custom_logging.error("Redis not initalized")
                return False
            
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
            custom_logging.error(f"Redis get error: {e}")
            trace_back = e.__traceback__
            custom_logging.error(f"Traceback to line no. {trace_back.tb_lineno}")
        
        

