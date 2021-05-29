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
        unique=True,
    )


def save2db(txt_str: Optional[Union[WordType, SentenceType, DocumentType]]) -> TextString:
    try:
        s = String.objects.filter(public_key=txt_str.alias).first()
        if s is not None:
            return s
        s = TextString()
        s.public_key = txt_str.alias
        s.type = type(txt_str)
        s.save()
        return s
    except:
        raise Exception('input value type is not permitted.')
