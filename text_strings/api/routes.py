import json
from os.path import join

from django.views.decorators.http import require_POST
from django.http import HttpRequest

from text_strings.api.forms import *
from repository.decorators import response, response2
from .controlers import word2db, sentence2db, document2db, keywords_extract


@require_POST
@response2(Word2DBInput, Word2DBOutput)
def words2db_view(input_fields):
    return word2db(input_fields['word'])


@require_POST
@response2(Sentences2DBInput, Sentences2DBOutput)
def sentences2db_view(input_fields):
    return sentence2db(input_fields['sentence'])


@require_POST
@response(Index2DBInput, Index2DBOutput)
def index2db_view(input_fields, output_fields):
    pass


@require_POST
@response(IndexInput, IndexOutput)
def index_view(input_fields, output_fields):
    pass


@require_POST
@response(IsIndexInput, IsIndexOutput)
def is_index_view(input_fields, output_fields):
    pass


@require_POST
@response2(Documents2DBInput, Documents2DBOutput)
def documents2db_view(input_fields):
    return document2db(input_fields['document'])


@require_POST
@response(Keywords2DBInput, Keywords2DBOutput)
def keywords2db_view(input_fields, output_fields):
    pass


@require_POST
@response2(KeywordsInput)
def keywords_view(input_fields):
    res = keywords_extract(input_fields['document'])
    return res


@require_POST
@response(IsKeywordsInput, IsKeywordsOutput)
def is_keywords_view(input_fields, output_fields):
    pass


@require_POST
@response(Stopwords2DBInput, Stopwords2DBOutput)
def stopwords2db_view(input_fields, output_fields):
    pass


@require_POST
@response(StopwordsInput, StopwordsOutput)
def stopwords_view(input_fields, output_fields):
    pass


@require_POST
@response(IsStopwordsInput, IsStopwordsOutput)
def is_stopwords_view(input_fields, output_fields):
    pass


@require_POST
@response(NormalizeInput, NormalizeOutput)
def normalize_view(input_fields, output_fields):
    pass


@require_POST
@response(TokenizeInput, TokenizeOutput)
def tokenize_view(input_fields, output_fields):
    pass


@require_POST
@response(DocumentInput, DocumentOutput)
def document_view(input_fields, output_fields):
    from .controlers import document_analysis
    return document_analysis(input_fields, output_fields)
