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
        return similar(self.__str__(), str(other))

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
        return [self._value]

    @property
    def words(self):
        return [self._value]

    @property
    def alias(self):
        return to_hash(self._value)


class SentenceType:
    def __init__(self, value: Optional[Union[str, List[WordType]]]):
        self.value = value

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if type(val) == str:
            tokens = tokenizer_s2w(val)
            _value = []
            for token in tokens:
                _value.append(WordType(token))
            self._value = _value

        elif type(val) == list:
            for sub_val in val:
                if type(sub_val) != WordType:
                    raise Exception('error: value not correct.')
            self._value = val
        else:
            raise Exception('error: value not correct.')

    def __str__(self):
        _str = ''
        for wrd in self.value[:-1]:
            _str += f'{wrd} '
        _str += f'{self.value[-1]}'
        return _str

    def __eq__(self, other):
        return similar(self.__str__(), str(other))

    def __repr__(self):
        return repr(self.value)

    _tokens = None

    @property
    def tokens(self):
        if self._tokens is not None:
            return self._tokens
        _tokens = []
        for wrds in self.value:
            _tokens.append(wrds.tokens[0])

        self._tokens = _tokens
        return self._tokens

    _words = None

    @property
    def words(self):
        if self._words is not None:
            return self._words
        _words = []
        for wrd in self.value:
            wrd = wrd.words[0]
            if wrd not in _words:
                _words.append(wrd)

        self._words = _words
        return self._words

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
    def __init__(self, value: Optional[Union[str, List[SentenceType]]]):
        self.value = value

    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if type(val) == str:
            tokens = tokenizer_s2w(val)
            _value = []
            for token in tokens:
                _value.append(SentenceType(token))
            self._value = _value
            return
        elif type(val) == list:
            for sub_val in val:
                if type(sub_val) != SentenceType:
                    raise Exception('error: value not correct.')
            self._value = val
        else:
            raise Exception('error: value not correct.')

    def __str__(self):
        _str = ''
        for sent in self.value[:-1]:
            _str += f'{sent} '
        _str += f'{self.value[-1]}'
        return _str

    def __eq__(self, other):
        return similar(self.__str__(), str(other))

    def __repr__(self):
        return repr(self.value)

    _tokens = None

    @property
    def tokens(self):
        if self._tokens is not None:
            return self._tokens
        _tokens = []
        for wrds in self.value:
            __tokens = []
            for wrd in wrds.tokens:
                __tokens.append(wrd)
            _tokens.append(__tokens)
        self._tokens = _tokens
        return self._tokens

    _words = None

    @property
    def words(self):
        if self._words is not None:
            return self._words
        _words = []
        for wrds in self.value:
            for wrd in wrds.words:
                if wrd not in _words:
                    _words.append(wrd)
        self._words = _words
        return self._words

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
