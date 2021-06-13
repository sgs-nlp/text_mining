import json
import os.path

# from repository.data_frame import Word, Sentence, Document
from repository.types import WordType, SentenceType, DocumentType,CorpusType
from text_strings.models import (
    save2db,
    keywords_save2db,
    TextString,
    DocumentKeyword,
    user_scoring_keyword_save2db,
    keyword_save2db,
)
from repository.extractor import Keywords, Stopwords

from text_strings.serializer import keywords_to_dict

stopword_list = Stopwords()
stopword_list = stopword_list.STOPWORDSLIST


def word2db(word: str):
    word = WordType(word)
    word = save2db(word)
    return dict(word)


def sentence2db(sentence: str):
    sentence = SentenceType(sentence)
    sentence = save2db(sentence)
    return dict(sentence)


def document2db(document: str):
    document = DocumentType(document)
    document = save2db(document)
    return dict(document)


def keywords_extract(document: str):
    document = DocumentType(document)
    keyword_extractor = Keywords(stopwords_list=stopword_list, keywords_number=5, minimum_frequency=0.3)
    keywords = keyword_extractor.by_frequency(document=document.tokens)
    keywords = [WordType(keyword) for keyword in keywords]
    return keywords_save2db(document, keywords)


def document_keywords(document_id: str):
    document = TextString.objects.filter(pk=document_id).first()
    keywords = DocumentKeyword.objects.filter(document=document).all()
    keywords = [keyword for keyword in keywords]
    return keywords_to_dict(document, keywords)


def is_keywords(user_id: str, keywords_score_list: dict):
    for keyword_id, is_keyword in keywords_score_list.items():
        user_scoring_keyword_save2db(user_id, keyword_id, is_keyword)
    return {}


def keyword2db(document_id: str, word: str):
    word = WordType(word)
    return keyword_save2db(document_id, word)


def corpus2db(corpus_path: str):
    corpus = CorpusType(corpus_path)
    corpus = save2db(corpus)
    return dict(corpus)


def stopwords_list2db(corpus_path: str):
    corpus = CorpusType(corpus_path)
    corpus = save2db(corpus)
    return dict(corpus)



def document_analysis(input_fields, output_fields):
    pass
# def document_analysis(input_fields, output_fields):
#     string = ''
#     document_path = None
#     if len(input_fields['document_path']):
#         document_path = input_fields['document_path']
#         with open(document_path, 'r', encoding='utf-8') as file:
#             if file is None:
#                 raise Exception('file is not exist')
#             string = file.read()
#     elif len(input_fields['document']):
#         string = input_fields['document']
#
#     d = Document(string)
#     if not d.is_valid:
#         raise Exception('data is not valid')
#
#     if document_path is not None:
#         dir_name = os.path.dirname(document_path)
#         file_name = os.path.basename(document_path)
#         file_name_split = os.path.splitext(file_name)
#         name = file_name_split[0]
#         ext = file_name_split[1]
#     else:
#         from text_mining.settings import BASE_DIR
#         from datetime import datetime
#         dir_name = os.path.join(BASE_DIR, 'files')
#         name = str(hash(datetime.now()))
#         ext = '.file'
#     output = {'id': d.id}
#     if output_fields['normal_document_path'] is True:
#         normal_document_path = os.path.join(dir_name, f'{name}.normal{ext}')
#         with open(normal_document_path, 'w', encoding='utf-8') as file:
#             file.write(d.document)
#         output['normal_document_path'] = normal_document_path
#
#     if output_fields['normal_document'] is True:
#         output['normal_document'] = d.document
#
#     if output_fields['sentence_tokenize'] is True:
#         output['sentence_tokenize'] = d.sentences
#
#     if output_fields['word_tokenize'] is True:
#         output['word_tokenize'] = d.words
#
#     if output_fields['stop_words_list'] is True:
#         output['stop_words_list'] = d.stopwords
#
#     if output_fields['key_words_list'] is True:
#         output['key_words_list'] = d.keywords
#
#     if output_fields['save_to_file'] is True:
#         output_path = os.path.join(dir_name, f'{name}.output.json')
#         j_output = json.dumps(output)
#         with open(output_path, 'w') as file:
#             file.write(j_output)
#         output['result_file_path'] = str(output_path)
#
#     return output
