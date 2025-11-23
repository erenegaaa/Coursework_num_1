from typing import Dict, Union


def some_function() -> Dict[str, Union[str, int, float, None]]:
    params: Dict[str, Union[str, int, float, None]] = {
        "key1": "value1",
        "key2": 123,
        "key3": None
    }
    return params
