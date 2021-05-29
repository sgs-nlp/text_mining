from django.urls import path, include
from . import routes

app_name = 'text_string_api'

urlpatterns = [
    path('words/add', routes.words2db_view),

    path('sentences/add', routes.sentences2db_view),
    path('sentence/index/add', routes.index2db_view),
    path('sentence/index', routes.index_view),
    path('sentence/index/update', routes.is_index_view),


    path('documents/add', routes.documents2db_view),
    path('document/keywords/add', routes.keywords2db_view),
    path('document/keywords/list', routes.keywords_view),
    path('document/keywords/update', routes.is_keywords_view),


    path('corpus/stopwords/add', routes.stopwords2db_view),
    path('corpus/stopwords/list', routes.stopwords_view),
    path('corpus/stopwords/update', routes.is_stopwords_view),

    path('normalize', routes.normalize_view),
    path('tokenize', routes.tokenize_view),



    # path('', routes._view),
    # path('', routes._view),
    # path('', routes._view),
    # path('', routes._view),
    #

    path('document', routes.document_view),
]
