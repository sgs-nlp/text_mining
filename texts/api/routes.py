import json

from django.views.decorators.http import require_POST
from texts.api.forms import DocumentInput, DocumentOutput
from texts.api.controlers import Document
from repository.decorators import response
from django.http import HttpRequest
from text_mining.settings import MEDIA_FOLDER_NAME
from os.path import join
from repository.converter import to_query_dict


# @require_POST
# @response
# def document_view(request: HttpRequest):
#     d_input = DocumentInput(request.POST)
#     if not d_input.is_valid():
#         raise Exception(str(d_input.errors))
#     data = d_input.cleaned_data
#     document_path = data['document_path']
#     with open(document_path, 'r', encoding='utf-8') as file:
#         if file is None:
#             raise Exception('file is not exist')
#         string = file.read()
#     d = Document(string)
#     if not d.is_valid:
#         raise Exception('data is not valid')
#     normal_document_path = join(MEDIA_FOLDER_NAME, document_path.split('/')[-1])
#     with open(join(MEDIA_FOLDER_NAME, f'normal_{document_path.split("/")[-1]}'), 'w', encoding='utf-8') as file:
#         file.write(d.document)
#
#     output_fields = eval(data['output_fields'])
#     output = {}
#     if output_fields['normal_document_path']:
#         output['normal_document_path'] = normal_document_path
#
#     if output_fields['sentence_tokenize']:
#         output['sentence_tokenize'] = d.sentences
#
#     if output_fields['word_tokenize']:
#         output['word_tokenize'] = d.words
#
#     if output_fields['stop_words_list']:
#         output['stop_words_list'] = d.stopwords
#
#     if output_fields['key_words_list']:
#         output['key_words_list'] = d.keywords
#     return output


@require_POST
@response(DocumentInput, DocumentOutput)
def document_view(input_fields, output_fields):
    from .controlers import document_analysis
    return document_analysis(input_fields, output_fields)


