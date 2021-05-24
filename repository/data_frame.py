from typing import Optional
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


class Corpus:
    def __init__(self, data):
        self._id = None
        self._data = data
        self._corpus = None
        self._documents = None
        self._sentences = None
        self._words = None
        self._stopwords = None
        self._classes = None

    @property
    def id(self):
        return self.add_to_db()

    @property
    def is_valid(self) -> bool:
        return True

    def add_to_db(self):
        if not self.is_valid:
            return None
        # todo create cor2db
        self._id = 1
        return self._id

    @property
    def stopwords(self) -> Optional[list]:
        if not self.is_valid:
            return None
        return self._stopwords

    @stopwords.setter
    def stopwords(self, value):
        # todo check true stopwords
        self._stopwords = value

    def stop_word_list_extract(self):
        # todo create stopword list
        return []

    @property
    def words(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._words is not None:
            return self._words
        from hazm import WordTokenizer
        h_w_tokenizer = WordTokenizer()
        _docs = []
        for doc in self.sentences:
            _sents = []
            for sent in doc:
                _sents.append(h_w_tokenizer.tokenize(sent))
            _docs.append(_sents)
        self._words = _docs
        return self._words

    @property
    def sentences(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._sentences is not None:
            return self._sentences
        from hazm import SentenceTokenizer
        h_s_tokenizer = SentenceTokenizer()
        sents = []
        for doc in self.documents:
            sents.append(h_s_tokenizer.tokenize(doc))
        self._sentences = sents
        return self._sentences

    @property
    def documents(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._documents is not None:
            return self._documents
        self._documents = self.corpus
        return self._documents

    @property
    def corpus(self) -> Optional[list]:
        if not self.is_valid:
            return None
        if self._corpus is not None:
            return self._corpus
        _crp = []
        for doc in self._data:
            doc = edit_symbol_spacing(doc)
            _crp.append(h_normalizer.normalize(doc))
        self._corpus = _crp
        return self._corpus

    def to_dict(self):
        if not self.is_valid:
            return None
        return {
            'id': self.id,
            'words': self.words,
            'stop_words': self.keywords,
            'sentences': self.sentences,
            'documents': self.documents,
            'corpus': self.corpus,
        }


class Document:
    def __init__(self, string):
        self._id = None
        self._string = string
        self._document = None
        self._sentences = None
        self._words = None
        self._stopwords = None
        self._keywords = None

    @property
    def id(self):
        return self.add_to_db()

    @property
    def is_valid(self) -> bool:
        return True

    def add_to_db(self):
        if not self.is_valid:
            return None
        if self._id is not None:
            return self._id
        doc = document2db(self.words)
        self._id = doc.id
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
        # todo stop words ?
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
        string = edit_symbol_spacing(self._string)
        self._document = h_normalizer.normalize(string)
        return self._document

    def to_dict(self):
        if not self.is_valid:
            return None
        return {
            'id': self.id,
            'words': self.words,
            'key_words': self.keywords,
            'sentences': self.sentences,
            'document': self.document,

        }


class Sentence:
    def __init__(self, string):
        self._string = string
        self._sentence = None
        self._words = None
        self._id = None
        self._index_word_sentence = None

    @property
    def is_valid(self):
        return True

    @property
    def id(self):
        if not self.is_valid:
            return None
        return self.add_to_db()

    def add_to_db(self):
        if self._id is not None:
            return self._id
        from texts.models import sentence2db
        snt = document2db(self.sentence)
        self._id = snt.id
        return self._id

    @property
    def index_word_sentence(self):
        if not self.is_valid:
            return None
        if self._index_word_sentence is not None:
            return self._index_word_sentence
        # todo extract word index
        self._index_word_sentence = self.words[0]
        return self._index_word_sentence

    @property
    def words(self):
        if not self.is_valid:
            return None
        if self._words is not None:
            return self._words
        from hazm import WordTokenizer
        h_w_tokenizer = WordTokenizer()
        self._words = h_w_tokenizer.tokenize(self.sentence)
        return self._words

    @property
    def sentence(self):
        if not self.is_valid:
            return None
        if self._sentence is not None:
            return self._sentence
        self._sentence = h_normalizer.normalize(self._string)
        return self._sentence

    def to_dict(self):
        if not self.is_valid:
            return None
        return {
            'id': self.id,
            'words': self.words,
            'index_word_sentence': self.index_word_sentence,
            'sentence': self.sentence,
        }


class Word:
    def __init__(self, string):
        self._string = string
        self._word = None
        self._id = None

    @property
    def is_valid(self):
        return True

    @property
    def id(self):
        if not self.is_valid:
            return None
        return self.add_to_db()

    def add_to_db(self):
        if not self.is_valid:
            return None
        if self._id is not None:
            return self._id
        from texts.models import word2db
        wrd = word2db(self.word)
        self._id = wrd.id
        return self._id

    @property
    def word(self):
        if not self.is_valid:
            return None
        if self._word is not None:
            return self._word
        self._word = h_normalizer.normalize(self._string)
        return self._word

    def to_dict(self):
        if not self.is_valid:
            return None
        return {
            'id': self.id,
            'word': self.word,
        }
