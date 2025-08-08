import time
import functools
import asyncio
import logging
from typing import Callable, List

# Setup logging
logging.basicConfig(
    filename='info.log', level=logging.INFO, 
    filemode="a", format='[%(levelname)s] %(message)s'
)



def calculate_execution_time(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start
            logging.info(f"{func.__name__} executed in {duration:.2f} seconds.")
            return result
        return wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            logging.info(f"{func.__name__} executed in {duration:.2f} seconds.")
            return result
        return wrapper