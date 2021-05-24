import json
from os.path import join

from django.views.decorators.http import require_POST
from django.http import HttpRequest

from texts.api.forms import DocumentInput, DocumentOutput
from repository.decorators import response


@require_POST
@response(DocumentInput, DocumentOutput)
def document_view(input_fields, output_fields):
    from .controlers import document_analysis
    return document_analysis(input_fields, output_fields)
