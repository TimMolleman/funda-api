from typing import Callable


def query(query_func: Callable) -> Callable:
    """Wrapper for queries. Raises exception if there is one, otherwise simply executes query."""
    def run_query(*args, **kwargs):
        try:
            return query_func(*args, **kwargs)
        except Exception as e:
            raise e

    return run_query
