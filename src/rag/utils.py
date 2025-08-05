import time
import logging
from typing import Callable, List

# Setup logging
logging.basicConfig(
    filename='info.log', level=logging.INFO, 
    filemode="a", format='[%(levelname)s] %(message)s'
)


def calculate_execution_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function {func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper
