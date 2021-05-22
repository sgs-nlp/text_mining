from functools import wraps
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_POST
from texts.api.forms import DocumentInput
from texts.api.controlers import Document
from django.http import HttpRequest
from text_mining.settings import MEDIA_FOLDER_NAME
from os.path import join


def _response():
    def decorator(function):
        @wraps(function)
        def wrap(request: HttpRequest, *args, **kwargs):
            try:
                result = function(request, *args, **kwargs)
                return JsonResponse({
                    'success': True,
                    'message': None,
                    'data': result,
                })

            except Exception as ex:
                return JsonResponse({
                    'success': False,
                    'message': ex.args,
                    'data': None,
                })

        return wrap

    return decorator


response = _response()

# def clean_data(data: HttpRequest) -> [dict, dict]:
#     _input = None
#     _output = None
#
#     d_input = DocumentInput(data)
#     if not d_input.is_valid():
#         raise Exception(str(d_input.errors))
#     _input = d_input.cleaned_data
#     d_output = DocumentOutput(data)
#     if not d_output.is_valid():
#         raise Exception(str(d_output.errors))
#
#     return _input, _output
