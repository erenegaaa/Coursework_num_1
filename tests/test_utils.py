import pandas as pd
import tempfile
import os

def create_test_csv_file():
    """Создание тестового CSV файла для проверки"""
    test_data = {
        'ID': [1, 2, 3],
        'Дата': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'Сумма': [1000, 2500, 300],
        'Описание': [
            'Оплата заказчику +79161234567',
            'Перевод 8-916-765-43-21 за услуги',
            'Возврат средств'
        ],
        'Категория': ['Расход', 'Расход', 'Доход']
    }

    df = pd.DataFrame(test_data)
    temp_file = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
    df.to_csv(temp_file.name, index=False, encoding='utf-8')
    return temp_file.name