import json
import os.path
from typing import Optional
from repository.pre_processing import edit_symbol_spacing
from repository.extractor import Stopwords, Keywords
from texts.models import Word


class Document:
    def __init__(self, string):
        self.string = string
        self._document = None
        self._sentences = None
        self._words = None
        self._stopwords = None
        self._keywords = None
        # todo
        self._id = 1
        self.add_to_db_flag = True

    @property
    def id(self):
        return self.add_to_db()

    @property
    def is_valid(self) -> bool:
        return True

    def add_to_db(self):
        if not self.is_valid:
            return None
        if self.add_to_db_flag:
            return self._id
        # word to db
        _d_words = self.words
        for _s_words in _d_words:
            for _word in _s_words:
                if Word.objects.filter(char=_word).first() is None:
                    wrd = Word()
                    wrd.char = _word
                    wrd.save()
        # todo true id
        self._id = 1
        return self._id

    @property
    def keywords(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._keywords is not None:
            return self._keywords
        k = Keywords(stopwords_list=self.stopwords, minimum_frequency=0.3)
        self._keywords = k.by_frequency(document=self.words)
        return self._keywords

    @property
    def stopwords(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._stopwords is not None:
            return self._stopwords
        s = Stopwords()
        self._stopwords = []
        for words in self.words:
            for word in words:
                if s.is_stopword(word):
                    self._stopwords.append(word)
        return self._stopwords

    @property
    def words(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._words is not None:
            return self._words
        from hazm import WordTokenizer
        _doc = []
        h_w_tokenizer = WordTokenizer()
        for sentence in self.sentences:
            words = h_w_tokenizer.tokenize(sentence)
            _doc.append(words)
        self._words = _doc
        return self._words

    @property
    def sentences(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._sentences is not None:
            return self._sentences
        from hazm import SentenceTokenizer
        h_s_tokenizer = SentenceTokenizer()
        self._sentences = h_s_tokenizer.tokenize(self.document)
        return self._sentences

    @property
    def document(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._document is not None:
            return self._document
        from hazm import Normalizer
        h_normalizer = Normalizer(
            remove_extra_spaces=True,
            persian_style=True,
            persian_numbers=True,
            remove_diacritics=True,
            affix_spacing=True,
            token_based=True,
            punctuation_spacing=True
        )
        string = edit_symbol_spacing(self.string)
        self._document = h_normalizer.normalize(string)
        return self._document


# class Sentence:
#     def __init__(self, string):
#         self.string = string
#         self._sentence = None
#         self._words = None
#
#     @property
#     def is_valid(self):
#         return True
#
#     def add_to_db(self):
#         pass
#
#     def keywords(self):
#         pass
#
#     def stopwords(self):
#         pass
#
#     def words(self):
#         if self._words is not None:
#             return self._words
#         from hazm import WordTokenizer
#         _doc = []
#         h_w_tokenizer = WordTokenizer()
#         self._words = h_w_tokenizer.tokenize(self._sentence)
#         return self._words
#
#     def sentence(self):
#         if self._sentence is not None:
#             return self._sentence
#         from hazm import Normalizer
#         h_normalizer = Normalizer()
#         self._sentence = h_normalizer.normalize(self.string)
#         return self._sentence
#
#
# class Word:
#     def __init__(self, string):
#         self.string = string
#         self._word = None
#
#     @property
#     def is_valid(self):
#         return True
#
#     def add_to_db(self):
#         pass
#
#     def word(self):
#         if self._word is not None:
#             return self._word
#         from hazm import Normalizer
#         h_normalizer = Normalizer()
#         self._word = h_normalizer.normalize(self.string)
#         return self._word

def document_analysis(input_fields, output_fields):
    print(output_fields)
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
        print(j_output)
        with open(output_path, 'w') as file:
            file.write(j_output)
        output['result_file_path'] = str(output_path)

    return output
