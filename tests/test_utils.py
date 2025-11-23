import os
import tempfile
from typing import Generator

import pandas as pd
import pytest

from src.utils import df_to_json_serializable, dumps_json, extract_phone, read_transactions_from_excel


@pytest.fixture
def sample_excel_file() -> Generator[str, None, None]:
    """Создает тестовый Excel файл"""
    test_data = {
        'ID': [1, 2, 3],
        'Дата': pd.to_datetime(['2024-01-15', '2024-01-16', '2024-01-17']),
        'Сумма': [1000.50, 2500.00, 300.75],
        'Описание': [
            'Оплата заказчику +79161234567',
            'Перевод 8-916-765-43-21 за услуги',
            'Возврат средств'
        ],
        'Категория': ['Расход', 'Расход', 'Доход']
    }

    df = pd.DataFrame(test_data)
    temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    df.to_excel(temp_file.name, index=False, engine='openpyxl')
    temp_file.close()
    yield temp_file.name
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Создает тестовый DataFrame"""
    return pd.DataFrame({
        'ID': [1, 2],
        'Описание': ['Тест +79161234567', 'Другой тест'],
        'Сумма': [100, 200],
        'Дата': pd.to_datetime(['2024-01-01', '2024-01-02'])
    })


class TestReadTransactionsFromExcel:
    """Тесты для функции read_transactions_from_excel"""

    def test_read_valid_excel(self, sample_excel_file: str) -> None:
        """Тест чтения корректного Excel файла"""
        df = read_transactions_from_excel(sample_excel_file)
        assert len(df) == 3
        assert list(df.columns) == ['ID', 'Дата', 'Сумма', 'Описание', 'Категория']

    def test_read_with_sheet_name(self, sample_excel_file: str) -> None:
        """Тест чтения с указанием имени листа"""
        df = read_transactions_from_excel(sample_excel_file, sheet_name=0)
        assert len(df) == 3


class TestDfToJsonSerializable:
    """Тесты для функции df_to_json_serializable"""

    def test_dataframe_conversion(self, sample_dataframe: pd.DataFrame) -> None:
        """Тест преобразования DataFrame в JSON-совместимый формат"""
        json_data = df_to_json_serializable(sample_dataframe)
        assert len(json_data) == 2
        assert isinstance(json_data, list)
        assert all(isinstance(item, dict) for item in json_data)

    def test_timestamp_conversion(self) -> None:
        """Тест преобразования временных меток"""
        df = pd.DataFrame({
            'timestamp': [pd.Timestamp('2024-01-01 10:00:00')],
            'value': [100]
        })
        json_data = df_to_json_serializable(df)
        assert isinstance(json_data[0]['timestamp'], str)
        assert json_data[0]['timestamp'] == '2024-01-01 10:00:00'

    def test_nan_handling(self) -> None:
        """Тест обработки NaN значений"""
        df = pd.DataFrame({
            'id': [1],
            'empty': [None]
        })
        json_data = df_to_json_serializable(df)
        assert json_data[0]['empty'] is None


class TestDumpsJson:
    """Тесты для функции dumps_json"""

    def test_basic_serialization(self) -> None:
        """Тест базовой сериализации"""
        test_data = [{'id': 1, 'name': 'test'}]
        result = dumps_json(test_data)
        assert isinstance(result, str)
        assert '"id": 1' in result
        assert '"name": "test"' in result

    def test_ensure_ascii_false(self) -> None:
        """Тест сериализации с ensure_ascii=False"""
        test_data = [{'text': 'русский текст'}]
        result = dumps_json(test_data, ensure_ascii=False)
        assert 'русский текст' in result


class TestExtractPhone:
    """Тесты для функции extract_phone"""

    def test_valid_phone_numbers(self) -> None:
        """Тест извлечения валидных номеров телефонов"""
        test_cases = [
            ('Оплата +79161234567', '+79161234567'),
            ('Телефон 8-916-765-43-21', '89167654321'),
            ('+7 916 123 45 67', '+79161234567'),
            ('8(916)765-43-21', '89167654321')
        ]
        for text, expected in test_cases:
            result = extract_phone(text)
            assert result == expected

    def test_phone_extraction_from_dataframe(self, sample_dataframe: pd.DataFrame) -> None:
        """Тест извлечения телефонов из DataFrame"""
        phones = sample_dataframe['Описание'].apply(lambda x: extract_phone(str(x))).tolist()
        assert phones[0] == '+79161234567'
        assert phones[1] is None


class TestIntegration:
    """Интеграционные тесты"""

    def test_full_workflow(self, sample_excel_file: str) -> None:
        """Тест полного рабочего процесса"""
        df = read_transactions_from_excel(sample_excel_file)
        json_data = df_to_json_serializable(df)
        json_string = dumps_json(json_data)
        assert len(df) == len(json_data)
        assert isinstance(json_string, str)
        assert all('ID' in item for item in json_data)

    def test_phone_extraction_from_dataframe(self, sample_dataframe: pd.DataFrame) -> None:
        """Тест извлечения телефонов из DataFrame"""
        phones = sample_dataframe['Описание'].apply(extract_phone).tolist()
        assert phones[0] == '+79161234567'
        assert phones[1] is None
