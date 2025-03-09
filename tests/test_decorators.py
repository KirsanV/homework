import os

import pytest

from src.decorators import log

# Удаляем файл лога перед тестами
LOG_FILE = "mylog.txt"
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)


@log(filename=LOG_FILE)
def successful_function(a: int, b: int) -> int:
    """
    Складывает два числа.
    """
    return a + b


@log(filename=LOG_FILE)
def function_with_error(a: int, b: int) -> float:
    """
    ZeroDivisionError: Если b равно 0.
    """
    return a / b


def test_log_file_creation() -> None:
    """
    Тестирует создание файла лога.
    """
    successful_function(3, 4)
    assert os.path.exists(LOG_FILE)


def test_log_file_content() -> None:
    """
    Тестирует содержание файла лога при успешном вызове функции.
    """
    successful_function(5, 6)
    with open(LOG_FILE, 'r') as file:
        log_contents = file.read()
    assert "successful_function ok" in log_contents


def test_log_file_error_content(capsys) -> None:
    """
    Тестирует содержание файла лога при ошибочном вызове функции.
    """
    with pytest.raises(TypeError):
        successful_function(1, 's')  # Это вызовет TypeError
    with open(LOG_FILE, 'r') as file:
        log_contents = file.read()
    assert "successful_function error: TypeError. Inputs: (1, 's'), {}" in log_contents
