import functools
import logging
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.
    """

    # Настройки логирования
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if filename:
        handler = logging.FileHandler(filename)
    else:
        logg: logging.Handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Декоратор для записи логов вызовов функции.
        """
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обертка функции для обработки и логирования.
            """
            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
