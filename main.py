import requests
import json
import os
import re
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config(config_path: str = "config.json") -> dict[str, Any]:
    """Загружает конфигурацию из JSON файла с безопасной обработкой ошибок."""
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Ошибка: Файл {config_path} содержит невалидный JSON.")
        except PermissionError:
            logging.error(f"Ошибка: Нет прав для чтения файла {config_path}.")
        except Exception as e:
            logging.error(f"Неожиданная ошибка при чтении файла конфигурации: {e}")
    return {}

if __name__ == "__main__":
    logging.info("PainScout AI запущен.")
    config = load_config()
    logging.info(f"Конфигурация загружена: {bool(config)}")
