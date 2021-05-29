import json
import os.path

from repository.data_frame import Word, Sentence, Document
from repository.types import WordType, SentenceType, DocumentType
from text_strings.models import save2db


def word2db(word: str):
    word = WordType(word)
    return save2db(word)


# def word2db(word: str):
#     word = WordType(word)
#     return save2db(word)
#
#
# def word2db(word: str):
#     word = WordType(word)
#     return save2db(word)


def document_analysis(input_fields, output_fields):
    string = ''
    document_path = None
    if len(input_fields['document_path']):
        document_path = input_fields['document_path']
        with open(document_path, 'r', encoding='utf-8') as file:
            if file is None:
                raise Exception('file is not exist')
            string = file.read()
    elif len(input_fields['document']):
        string = input_fields['document']

    d = Document(string)
    if not d.is_valid:
        raise Exception('data is not valid')

    if document_path is not None:
        dir_name = os.path.dirname(document_path)
        file_name = os.path.basename(document_path)
        file_name_split = os.path.splitext(file_name)
        name = file_name_split[0]
        ext = file_name_split[1]
    else:
        from text_mining.settings import BASE_DIR
        from datetime import datetime
        dir_name = os.path.join(BASE_DIR, 'files')
        name = str(hash(datetime.now()))
        ext = '.file'
    output = {'id': d.id}
    if output_fields['normal_document_path'] is True:
        normal_document_path = os.path.join(dir_name, f'{name}.normal{ext}')
        with open(normal_document_path, 'w', encoding='utf-8') as file:
            file.write(d.document)
        output['normal_document_path'] = normal_document_path

    if output_fields['normal_document'] is True:
        output['normal_document'] = d.document

    if output_fields['sentence_tokenize'] is True:
        output['sentence_tokenize'] = d.sentences

    if output_fields['word_tokenize'] is True:
        output['word_tokenize'] = d.words

    if output_fields['stop_words_list'] is True:
        output['stop_words_list'] = d.stopwords

    if output_fields['key_words_list'] is True:
        output['key_words_list'] = d.keywords

    if output_fields['save_to_file'] is True:
        output_path = os.path.join(dir_name, f'{name}.output.json')
        j_output = json.dumps(output)
        with open(output_path, 'w') as file:
            file.write(j_output)
        output['result_file_path'] = str(output_path)

    return output
