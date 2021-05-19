from django.db import models


class Corpus(models.Model):
    documents = models.ManyToManyField(
        to='Document',
    )
    stopwords = models.ManyToManyField(
        to='StopWord',
    )
    keywords = models.ManyToManyField(
        to='KeyWord',
    )
    topics = models.ManyToManyField(
        to='Topic',
    )


class Document(models.Model):
    paragraphs = models.ManyToManyField(
        to='Paragraph',
    )
    stopwords = models.ManyToManyField(
        to='StopWord',
    )
    keywords = models.ManyToManyField(
        to='KeyWord',
    )
    topics = models.ManyToManyField(
        to='Topic',
    )


class Paragraph(models.Model):
    sentences = models.ManyToManyField(
        to='Sentence',
    )
    stopwords = models.ManyToManyField(
        to='StopWord',
    )
    keywords = models.ManyToManyField(
        to='KeyWord',
    )
    topics = models.ManyToManyField(
        to='Topic',
    )


class Sentence(models.Model):
    words = models.ManyToManyField(
        to='Word',
    )
    stopwords = models.ManyToManyField(
        to='StopWord',
    )
    keywords = models.ManyToManyField(
        to='KeyWord',
    )
    topics = models.ManyToManyField(
        to='Topic',
    )


class KeyWord(models.Model):
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
    )


class StopWord(models.Model):
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
    )


class Topic(models.Model):
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
    )


class Word(models.Model):
    char = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
    )
