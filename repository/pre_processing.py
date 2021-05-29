from typing import Optional
from hazm import WordTokenizer, SentenceTokenizer, Normalizer

h_normalizer = Normalizer(
    remove_extra_spaces=True,
    persian_style=True,
    persian_numbers=True,
    remove_diacritics=True,
    affix_spacing=True,
    token_based=True,
    punctuation_spacing=True
)
h_word_tokenier = WordTokenizer()
h_word_tokenier = h_word_tokenier.tokenize
h_sentence_tokenier = SentenceTokenizer()
h_sentence_tokenier = h_sentence_tokenier.tokenize


def edit_symbol_spacing(string: str) -> str:
    _str = ''
    for c in string:
        if _is_symbol(c):
            _str += f' {c} '
            continue
        _str += c
    return _str


def _is_symbol(character: str) -> bool:
    PERSIAN_SYMBOL = ['!', '"', '#', '(', ')', '*', ',', '-', '.', '/', ':', '[', ']', '«', '»', '،', '؛', '؟',
                      '+', '=', '_', '-', '&', '^', '%', '$', '#', '@', '!', '~', '"', "'", ':', ';', '>', '<',
                      '.', ',', '/', '\\', '|', '}', '{', '-', 'ـ', ]
    if character in PERSIAN_SYMBOL:
        return True
    return False


def normalizer(value: str) -> str:
    res = h_normalizer.normalize(value)
    return res


def tokenizer(value: str = None, mode: str = 'sentence2words') -> list:
    if value is None:
        raise Exception('value is none.')

    if mode == 'sentence2words' or mode == 's2w':
        res = h_word_tokenier(value)
    elif mode == 'document2sentences' or mode == 'd2s':
        res = h_sentence_tokenier(value)
    elif mode == 'documents2words' or mode == 'd2w':
        sents = h_sentence_tokenier(value)
        res = []
        for sent in sents:
            res.append(h_word_tokenier(sent))
    else:
        raise Exception('mode is not correct.')
    return res


def tokenizer_s2w(value: str) -> list:
    return h_word_tokenier(value)


def tokenizer_d2s(value: str) -> list:
    return h_sentence_tokenier(value)


def tokenizer_d2w(value: str) -> list:
    sents = h_sentence_tokenier(value)
    res = []
    for sent in sents:
        res.append(h_word_tokenier(sent))
    return res
