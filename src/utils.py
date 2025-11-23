"""
Модуль для чтения Excel,
что в дальнейшем будет использоваться для Json файла транзакций.
"""
import json
import logging
import re
from typing import Any, Dict, List, Optional, Union

import pandas as pd

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def read_transactions_from_excel(path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
    """Считывание транзакции из excel файла"""
    logger.info("Чтение транзакции из %s (sheet=%s)", path, sheet_name)
    df = pd.read_excel(path, sheet_name=sheet_name)
    df.columns = [c.strip() if isinstance(c, str) else str(c) for c in df.columns]  # Исправлено
    return df


def df_to_json_serializable(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Преобразование Dataframe в список словарей для json"""
    result: List[Dict[str, Any]] = []  # Явно указываем тип
    for _, row in df.iterrows():
        obj: Dict[str, Any] = {}
        for col, value in row.items():
            if isinstance(value, pd.Timestamp):
                obj[str(col)] = value.strftime("%Y-%m-%d %H:%M:%S")  # Исправлено: str(col)
            elif pd.isna(value):
                obj[str(col)] = None  # Исправлено: str(col)
            else:
                obj[str(col)] = value  # Исправлено: str(col)
        result.append(obj)
    return result


def dumps_json(obj: Any, ensure_ascii: bool = False) -> str:
    """Обертка json файла"""
    logger.debug("Перепись файла в JSON формат")
    return json.dumps(obj, ensure_ascii=ensure_ascii, indent=2)


PHONE_RE = re.compile(r'(\+?\d{1,3}[\s\-]?)?(\(?\d{3,4}\)?[\s\-]?)?[\d\-\s]{5,}')


def extract_phone(text: Optional[str]) -> Optional[str]:
    """Поиск номера телефона в тексте транзакции"""
    if not text or not isinstance(text, str):
        return None
    m = PHONE_RE.search(text)
    if m:
        phone = m.group(0)
        cleaned = re.sub(r'[^\d+]', '', phone)
        logger.debug("Извлечен номер телефона %s из файла %s", cleaned, text)
        return cleaned
    return None
