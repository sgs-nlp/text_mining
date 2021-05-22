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

    @property
    def is_valid(self) -> bool:
        return True

    def add_to_db(self):
        if not self.is_valid:
            return None
        # word to db
        _d_words = self.words
        for _s_words in _d_words:
            for _word in _s_words:
                if Word.objects.filter(char=_word).first() is None:
                    wrd = Word()
                    wrd.char = _word
                    wrd.save()

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
