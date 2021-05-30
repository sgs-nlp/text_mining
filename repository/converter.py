import json

from django.http import QueryDict
import json


def to_query_dict(value: str) -> QueryDict:
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


def to_hash(value: str) -> str:
    return hash(value)

# def to_hash(value: str, string_type: str = None) -> str:
#     if string_type is None or string_type == 'word' or string_type == 'w':
#         return hash(f'{value}')
#     elif string_type == 's' or string_type == 'sent' or string_type == 'sentence':
#         string = ''
#         for word in value:
#             string += f'{word}'
#         return hash(string)
#     elif string_type == 'd' or string_type == 'doc' or string_type == 'document':
#         string = ''
#         for sent in value:
#             for word in sent:
#                 string += f'{word}'
#         return hash(f'{value}')
#     elif string_type == 'c' or string_type == 'crp' or string_type == 'corpus':
#         string = ''
#         for doc in value:
#             for sent in doc:
#                 for word in sent:
#                     string += f'{word}'
#         return hash(f'{value}')
#     else:
#         return None
