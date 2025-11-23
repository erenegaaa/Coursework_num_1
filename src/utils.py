"""
Модуль для чтения Excel,
что в дальнейшем будет использоваться для Json файла транзакций.
"""

from typing import List, Dict, Any
import json
import logging
from datetime import datetime
import pandas as pd
import re


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def read_transaction_from_excel(path: str, sheet_name: str=0) -> pd.DataFrame:
    """Считывание транзакции из excel файла"""
    logger.info("Чтение транзакции из %s (sheet=%s)")
    df = pd.read_excel(path, sheet_name=sheet_name)
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns] # один регистр
    return df


def df_to_json_serializable(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Преобразование Dataframe в список словарей для json"""
    result = []
    for _, row in df.iterrows():
        obj = {}
        for col, value in row.items():
            if isinstance(value, (pd.Timestamp, pd.DataFrame)):
                obj[col] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif pd.isna(value):
                obj[col] = None
            else:
                obj[col] = value
        result.append(obj)
    return result


def dumps_json():
    """обертка json файла"""
    pass


def extract_phone():
    """Поиск номера телефона в тексте транзакции"""
    pass