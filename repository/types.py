from typing import Optional, Union, List
from repository.text_similarity import similar
from repository.pre_processing import normalizer, tokenizer_s2w, tokenizer_d2s
from repository.converter import to_hash


class WordType:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return similar(self.alias, other.alias)

    def __repr__(self):
        return repr(self.value)

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = normalizer(val)

    @property
    def tokens(self):
        return self._value

    @property
    def words(self):
        return [self._value]

    @property
    def unique_words_list(self):
        return [self._value]

    @property
    def alias(self):
        return self._value


class SentenceType:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        _str = ''
        for wrd in self.value[:-1]:
            _str += f'{wrd} '
        _str += f'{self.value[-1]}'
        return _str

    def __eq__(self, other):
        return similar(self.alias, other.alias)

    def __repr__(self):
        return repr(self.value)

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        tokens = tokenizer_s2w(val)
        _value = []
        for token in tokens:
            _value.append(WordType(token))
        self._value = _value

    _tokens = None

    @property
    def tokens(self):
        if self._tokens:
            return self._tokens
        _tokens = []
        for wrd in self.value:
            _tokens.append(wrd.tokens)
        self._tokens = _tokens
        return self._tokens

    _words = None

    @property
    def words(self):
        if self._words:
            return self._words
        _words = []
        for wrd in self.value:
            _words += wrd.words
        self._words = _words
        return self._words

    _unique_words_list = None

    @property
    def unique_words_list(self):
        if self._unique_words_list:
            return self._unique_words_list
        _unique_words_list = []
        for wrd in self.value:
            for w in wrd.unique_words_list:
                if w not in _unique_words_list:
                    _unique_words_list.append(w)
        self._unique_words_list = _unique_words_list
        return self._unique_words_list

    _alias = None

    @property
    def alias(self):
        if self._alias is not None:
            return self._alias
        _alias = ''
        for wrd in self.value:
            _alias += f'{wrd.alias}-'
        self._alias = to_hash(_alias)
        return self._alias


class DocumentType:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        _str = ''
        for sent in self.value[:-1]:
            _str += f'{sent} '
        _str += f'{self.value[-1]}'
        return _str

    def __eq__(self, other):
        return similar(self.alias, other.alias)

    def __repr__(self):
        return repr(self.value)

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        tokens = tokenizer_d2s(val)
        _value = []
        for token in tokens:
            _value.append(SentenceType(token))
        self._value = _value

    _tokens = None

    @property
    def tokens(self):
        if self._tokens:
            return self._tokens
        _tokens = []
        for sent in self.value:
            _tokens.append(sent.tokens)
        self._tokens = _tokens
        return self._tokens

    _words = None

    @property
    def words(self):
        if self._words:
            return self._words
        _words = []
        for sent in self.value:
            _words += sent.words
        self._words = _words
        return self._words

    _unique_words_list = None

    @property
    def unique_words_list(self):
        if self._unique_words_list:
            return self._unique_words_list
        _unique_words_list = []
        for sent in self.value:
            for w in sent.unique_words_list:
                if w not in _unique_words_list:
                    _unique_words_list.append(w)
        self._unique_words_list = _unique_words_list
        return self._unique_words_list

    _alias = None

    @property
    def alias(self):
        if self._alias is not None:
            return self._alias
        _alias = ''
        for sentence in self.value:
            _alias += f'{sentence.alias}-'
        self._alias = to_hash(_alias)
        return self._alias


class CorpusType:
    def __init__(self, file_path):
        self.file_path = file_path
        self.value = file_path

    def __str__(self):
        return str(self.file_path)

    def __eq__(self, other):
        return similar(self.alias, other.alias)

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, file_path):
        import zipfile
        crp = zipfile.ZipFile(file_path)
        docs = crp.namelist()
        docs = docs[1:]
        _crp = []
        for doc in docs:
            with crp.open(doc) as file:
                doc = file.read()
            doc = doc.decode('utf-8')
            _crp.append(DocumentType(doc))
        self._value = _crp

    _tokens = None

    @property
    def tokens(self):
        if self._tokens:
            return self._tokens
        _tokens = []
        for doc in self.value:
            _tokens.append(doc.tokens)
        self._tokens = _tokens
        return self._tokens

    _words = None

    @property
    def words(self):
        if self._words:
            return self._words
        _words = []
        for doc in self.value:
            _words += doc.words
        self._words = _words
        return self._words

    _unique_words_list = []

    @property
    def unique_words_list(self):
        if self._unique_words_list:
            return self._unique_words_list
        _unique_words_list = []
        for doc in self.value:
            for w in doc.unique_words_list:
                if w not in _unique_words_list:
                    _unique_words_list.append(w)
        self._unique_words_list = _unique_words_list
        return self._unique_words_list

    _alias = None

    @property
    def alias(self):
        if self._alias is not None:
            return self._alias
        _alias = ''
        for doc in self.value:
            _alias += f'{doc.alias}-'
        self._alias = to_hash(_alias)
        return self._alias
