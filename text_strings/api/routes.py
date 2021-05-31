import json
from os.path import join

from django.views.decorators.http import require_POST
from django.http import HttpRequest

from repository.decorators import response, response2
from repository.converter import to_pydict
from .forms import *
from .controlers import (
    word2db,
    sentence2db,
    document2db,
    keywords_extract,
    document_keywords,
    is_keywords,
    keyword2db,
)


@require_POST
@response2(Word2DBInput, Word2DBOutput)
def words2db_view(input_fields):
    return word2db(input_fields['word'])


@require_POST
@response2(Sentences2DBInput, Sentences2DBOutput)
def sentences2db_view(input_fields):
    return sentence2db(input_fields['sentence'])


# todo
@require_POST
@response(Index2DBInput, Index2DBOutput)
def index2db_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(IndexInput, IndexOutput)
def index_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(IsIndexInput, IsIndexOutput)
def is_index_view(input_fields, output_fields):
    pass


@require_POST
@response2(Documents2DBInput, Documents2DBOutput)
def document2db_view(input_fields):
    return document2db(input_fields['document'])


@require_POST
@response2(Keywords2DBInput)
def keyword2db_view(input_fields):
    return keyword2db(input_fields['document_id'], input_fields['word'])


@require_POST
@response2(KeywordsInput)
def keywords_view(input_fields):
    return document_keywords(input_fields['document_id'])


@require_POST
@response2(KeywordsExtractorInput)
def keywords_extractor_view(input_fields):
    return keywords_extract(input_fields['document'])


@require_POST
@response2(IsKeywordsInput)
def is_keywords_view(input_fields):
    keywords_score_list = input_fields['keywords_score_list']
    keywords_score_list = to_pydict(keywords_score_list)
    return is_keywords(
        user_id=input_fields['user_id'],
        keywords_score_list=keywords_score_list
    )


# todo
@require_POST
@response(Stopwords2DBInput, Stopwords2DBOutput)
def stopwords2db_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(StopwordsInput, StopwordsOutput)
def stopwords_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(IsStopwordsInput, IsStopwordsOutput)
def is_stopwords_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(NormalizeInput, NormalizeOutput)
def normalize_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(TokenizeInput, TokenizeOutput)
def tokenize_view(input_fields, output_fields):
    pass


# todo
@require_POST
@response(DocumentInput, DocumentOutput)
def document_view(input_fields, output_fields):
    from .controlers import document_analysis
    return document_analysis(input_fields, output_fields)
