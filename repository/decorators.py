from functools import wraps
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_POST
from texts.api.forms import DocumentInput
from texts.api.controlers import Document
from django.http import HttpRequest
from text_mining.settings import MEDIA_FOLDER_NAME
from os.path import join
from repository.converter import to_query_dict


def response(input_rule=None, output_rule=None):
    def decorator(function):
        @wraps(function)
        def wrap(request: HttpRequest, *args, **kwargs):
            try:
                input_fields = {}
                if input_rule is not None:
                    input_fields = input_rule(request.POST)
                if not input_fields.is_valid():
                    raise Exception(str(input_fields.errors))
                input_fields = input_fields.cleaned_data
                output_fields = {}
                if input_rule is not None:
                    if 'output_fields' in request.POST:
                        output_fields = output_rule(to_query_dict(request.POST['output_fields']))
                        if not output_fields.is_valid():
                            raise Exception(str(output_fields.errors))
                        output_fields = output_fields.cleaned_data
                result = function(input_fields, output_fields)
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
