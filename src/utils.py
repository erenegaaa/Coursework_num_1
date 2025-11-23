"""
Модуль для чтения Excel,
что в дальнейшем будет использоваться для Json файла транзакций.
"""

from typing import List, Dict, Any
import json
import logging
import numpy as np
import pandas as pd
import re
from datetime import datetime

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def read_transactions_from_excel(path: str, sheet_name: str=0) -> pd.DataFrame:
    """Считывание транзакции из excel файла"""
    logger.info("Чтение транзакции из %s (sheet=%s)", path, sheet_name)
    df = pd.read_excel(path, sheet_name=sheet_name)
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns] # один регистр
    return df


def df_to_json_serializable(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Преобразование Dataframe в список словарей для json"""
    result = []
    for _, row in df.iterrows():
        obj = {}
        for col, value in row.items():
            if isinstance(value, (pd.Timestamp, datetime)):
                obj[col] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif pd.isna(value):
                obj[col] = None
            elif isinstance(value, (np.integer, np.int64)):
                obj[col] = int(value)
            elif isinstance(value, (np.floating, np.float64)):
                obj[col] = float(value)
            else:
                obj[col] = value
        result.append(obj)
    return result


def dumps_json(obj: Any, ensure_ascii: bool = False) -> str:
    """Обертка json файла"""
    logger.debug("Перепись файла в JSON формат")
    return json.dumps(obj, ensure_ascii=ensure_ascii, indent=2)


PHONE_RE = re.compile(r'(\+?7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}')


def extract_phone(text: str) -> str | None:
    """Поиск номера телефона в тексте транзакции"""
    if not isinstance(text, str):
        return None
    m = PHONE_RE.search(text)
    if m:
        phone = m.group(0)
        cleaned = re.sub(r'[^\d+]', '', phone)
        logger.debug("Извлечен номер телефона %s из файла %s", cleaned, text)
        return cleaned
    return None
