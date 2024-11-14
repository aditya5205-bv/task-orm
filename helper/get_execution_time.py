from functools import wraps
from logs.custom_logging import custom_logging
import time

def get_execution_time_decorator(func):
    @wraps(func)
    def get_execution_time(*args, **kwargs):
        
        start_time = time.perf_counter()
        
        func(*args, **kwargs)
        
        end_time = time.perf_counter()
        
        custom_logging.info(f"=== Time taken to run function {func.__name__} is:" 
                            f"{end_time - start_time} seconds ===")
        
    return get_execution_time