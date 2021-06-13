from django.db import models
from repository.types import WordType, SentenceType, DocumentType, CorpusType
from typing import Optional, Union
from .serializer import keywords_to_dict
from text_mining.settings import THRESHOLD_OF_ACTIONS, MINIMUM_PARTICIPATION


# class NodeType(models.Model):
#     title = models.CharField(
#         max_length=128,
#     )
#     features = models.JSONField()
#
#
# class RelationType(models.Model):
#     title = models.CharField(
#         max_length=64,
#     )
#     parent = models.ForeignKey(
#         to='RelationType',
#         on_delete=models.CASCADE,
#     )
#     permitted_type4from_ = models.ForeignKey(
#         to='NodeType',
#         on_delete=models.CASCADE,
#         related_name='t_s_rt_pt_from',
#     )
#     permitted_type4to_ = models.ForeignKey(
#         to='NodeType',
#         on_delete=models.CASCADE,
#         related_name='t_s_rt_pt_to',
#     )
#     features = models.JSONField()
#
#
# class Node(models.Model):
#     public_key = models.CharField(
#         max_length=512,
#         unique=True,
#     )
#     type = models.ForeignKey(
#         to='NodeType',
#         on_delete=models.CASCADE,
#     )
#
#     def __iter__(self):
#         yield 'id', self.pk
#         yield 'public_key', self.public_key
#         yield 'type', dict(self.type)
#
#
# class Edge(models.Model):
#     from_ = models.ForeignKey(
#         to='Node',
#         on_delete=models.CASCADE,
#         related_name='t_s_e_from',
#     )
#     to_ = models.ForeignKey(
#         to='Node',
#         on_delete=models.CASCADE,
#         related_name='t_s_e_from',
#     )
#     relation_type = models.ForeignKey(
#         to='RelationType',
#         on_delete=models.CASCADE,
#     )
#
#     def __iter__(self):
#         yield 'id', self.pk
#         yield 'from', dict(self.from_)
#         yield 'to', dict(self.to_)
#         yield 'features', dict(self.features)


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


class CorpusStopword(models.Model):
    corpus = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='t_c_s_corpus',
    )
    stopword = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='t_c_s_stopword',
    )
    _is_stopword = models.BooleanField(
        default=True,
    )

    @property
    def is_stopword(self):
        all_user_score = UserScoringToCorpusStopword.objects.filter(stopword=self).all()
        if all_user_score is None:
            return self._is_stopword
        user_len = len(all_user_score)
        if user_len < MINIMUM_PARTICIPATION:
            return self._is_stopword
        score = 0
        for user_score in all_user_score:
            if user_score.is_stopword:
                score += 1

        if score / user_len >= THRESHOLD_OF_ACTIONS:
            self._is_stopword = True
            return self._is_stopword

        self._is_stopword = False
        return self._is_stopword

    def __iter__(self):
        yield 'id', self.pk
        yield 'is_stopword', self.is_stopword
        yield 'corpus', dict(self.corpus)
        yield 'word', dict(self.stopword)


class UserScoringToCorpusStopword(models.Model):
    user_id = models.CharField(
        max_length=512,
    )
    stopword = models.ForeignKey(
        to=CorpusStopword,
        on_delete=models.CASCADE,
    )
    is_stopword = models.BooleanField()

    def __iter__(self):
        yield 'id', self.pk
        yield 'user_id', self.user_id
        yield 'stopword', dict(self.stopword)
        yield 'is_stopword', self.is_stopword


def save2db(txt: Optional[Union[WordType, SentenceType, DocumentType, CorpusType]]) -> TextString:
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
    for word in keywords:
        word = save2db(word)
        keyword = DocumentKeyword.objects.filter(document=document).filter(keyword=word).first()
        if keyword is None:
            keyword = DocumentKeyword(document=document, keyword=word)
            keyword.save()
        _keywords.append(keyword)
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
