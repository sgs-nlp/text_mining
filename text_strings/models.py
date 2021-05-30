from django.db import models
from repository.types import WordType, SentenceType, DocumentType
from typing import Optional, Union


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
        yield 'type', self.type


class TextStringRelation(models.Model):
    parent = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='text_string_parent',
    )
    child = models.ForeignKey(
        to='TextString',
        on_delete=models.CASCADE,
        related_name='text_string_child',
    )
    order = models.IntegerField(
        unique=False,
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
