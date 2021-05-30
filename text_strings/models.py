from django.db import models
from repository.types import WordType, SentenceType, DocumentType
from typing import Optional, Union
from .serializer import keywords_to_dict


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


class Keyword(models.Model):
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
        keyword = Keyword(document=document, keyword=keyword)
        keyword.save()
        _keywords.append(keyword.keyword)
    keywords = _keywords
    return keywords_to_dict(document, keywords)
