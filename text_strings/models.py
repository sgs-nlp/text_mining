from django.db import models
from repository.types import WordType, SentenceType, DocumentType
from typing import Optional, Union
from .serializer import keywords_to_dict
from text_mining.settings import THRESHOLD_OF_ACTIONS, MINIMUM_PARTICIPATION


class TextString(models.Model):
    public_key = models.CharField(
        max_length=512,
        unique=True,
    )
    type = models.CharField(
        max_length=32,
    )

    def __iter__(self):
        yield 'id', self.pk
        yield 'public_key', self.public_key
        yield 'type', str(self.type)


class TextStringRelation(models.Model):
    parent = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='t_s_tr_parent',
    )
    child = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='t_s_tr_child',
    )
    order = models.IntegerField(
        unique=False,
    )

    def __iter__(self):
        yield 'id', self.pk
        yield 'parent', dict(self.parent)
        yield 'child', dict(self.child)
        yield 'order', self.order


class DocumentKeyword(models.Model):
    document = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='t_s_k_document',
    )
    keyword = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='t_s_k_keyword',
    )
    _is_keyword = models.BooleanField(
        default=True,
    )

    @property
    def is_keyword(self):
        all_user_score = UserScoringToDocumentKeywords.objects.filter(keyword=self).all()
        if all_user_score is None:
            return self._is_keyword
        user_len = len(all_user_score)
        if user_len < MINIMUM_PARTICIPATION:
            return self._is_keyword
        score = 0
        for user_score in all_user_score:
            if user_score.is_keyword:
                score += 1

        if score / user_len >= THRESHOLD_OF_ACTIONS:
            self._is_keyword = True
            return self._is_keyword

        self._is_keyword = False
        return self._is_keyword

    def __iter__(self):
        yield 'id', self.pk
        yield 'is_keyword', self.is_keyword
        yield 'document', dict(self.document)
        yield 'word', dict(self.keyword)


class UserScoringToDocumentKeywords(models.Model):
    user_id = models.CharField(
        max_length=512,
    )
    keyword = models.ForeignKey(
        to=DocumentKeyword,
        on_delete=models.CASCADE,
    )
    is_keyword = models.BooleanField()

    def __iter__(self):
        yield 'id', self.pk
        yield 'user_id', self.user_id
        yield 'keyword', dict(self.keyword)
        yield 'is_keyword', self.is_keyword


def save2db(txt: Optional[Union[WordType, SentenceType, DocumentType]]) -> TextString:
    _text_string = TextString.objects.filter(public_key=txt.alias).first()
    if _text_string is not None:
        return _text_string
    _text_string = TextString()
    _text_string.public_key = txt.alias
    _text_string.type = type(txt)
    _text_string.save()
    if type(txt) == WordType:
        return _text_string
    for indx, itm in enumerate(txt.value):
        _sub_text_strings = save2db(itm)
        _text_string_relation = TextStringRelation()
        _text_string_relation.parent = _text_string
        _text_string_relation.child = _sub_text_strings
        _text_string_relation.order = indx
        _text_string_relation.save()
    return _text_string


def keywords_save2db(document: DocumentType, keywords: list) -> dict:
    document = save2db(document)
    _keywords = []
    for keyword in keywords:
        keyword = save2db(keyword)
        keyword = DocumentKeyword(document=document, keyword=keyword)
        keyword.save()
        _keywords.append(keyword.keyword)
    keywords = _keywords
    return keywords_to_dict(document, keywords)


def keyword_save2db(document_id: str, word: WordType) -> dict:
    word = save2db(word)
    keyword = DocumentKeyword.objects.filter(document_id=document_id).filter(keyword=word).first()
    if keyword is None:
        keyword = DocumentKeyword(document_id=document_id, keyword=word)
        keyword.save()
    return {'keyword': dict(keyword)}


def user_scoring_keyword_save2db(user_id: str, keyword_id: str, is_keyword):
    usk = UserScoringToDocumentKeywords.objects.filter(user_id=user_id).filter(keyword_id=keyword_id).first()
    if usk is None:
        usk = UserScoringToDocumentKeywords(user_id=user_id, keyword_id=keyword_id)
    usk.is_keyword = is_keyword
    usk.save()
    return usk
