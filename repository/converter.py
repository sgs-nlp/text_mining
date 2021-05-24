import json

from django.http import QueryDict
import json


def to_query_dict(value: str) -> QueryDict:
    value = json.loads(value)
    for k, v in value.items():
        value[k] = to_boolean(v)
    res = QueryDict('', mutable=True)
    res.update(value)
    return res


def to_boolean(value):
    if value == 'True' or value == 'true' or value == 1 or value == '1':
        return True
    if value == 'False' or value == 'false' or value == 0 or value == '0':
        return False
    return value
