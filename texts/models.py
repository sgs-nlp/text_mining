from django.db import models


class Corpus(models.Model):
    stop_words = models.ManyToManyField(
        to='Word',
        related_name='t_c_stop_words',
    )
    symbols = models.ManyToManyField(
        to='Word',
        related_name='t_c_stop_symbols',
    )
    classes = models.ManyToManyField(
        to='Class',
    )

    class Meta:
        verbose_name = 'Corpus'
        verbose_name_plural = 'Corpus'


class FeaturesDocumentCorpus(models.Model):
    corpus = models.ForeignKey(
        to='Corpus',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    document = models.ForeignKey(
        to='Document',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


class Document(models.Model):
    _sentences = None

    @property
    def sentence(self):
        if self._sentences is not None:
            return self._sentences
        document_sentences = FeaturesSentenceDocument.objects.filter(document=self.pk).all()
        document_first_sentence = document_sentences.filter(previous_sentence=None).first()
        first_sentence = document_first_sentence.sentence
        self._sentences = []
        self._sentences.append(first_sentence)
        next_sentence = document_first_sentence.next_sentence
        while next_sentence is not None:
            document_sentence = document_sentences.filter(sentence=next_sentence).first()
            sentence = document_sentence.sentence

            self._sentences.append(sentence)

            next_sentence = document_sentence.next_sentence
        return self._sentences

    key_words = models.ManyToManyField(
        to='Word',
    )

    def __str__(self):
        return f'{self.pk}'


class FeaturesSentenceDocument(models.Model):
    document = models.ForeignKey(
        to='Document',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    previous_sentence = models.ForeignKey(
        to='Sentence',
        on_delete=models.CASCADE,
        related_name='t_fsd_previous_sentence',
        null=True,
        blank=True,
    )
    sentence = models.ForeignKey(
        to='Sentence',
        on_delete=models.CASCADE,
        related_name='t_fsd_sentence',
        null=False,
        blank=False,
    )
    index_word_sentence = models.ForeignKey(
        to='Word',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    next_sentence = models.ForeignKey(
        to='Sentence',
        on_delete=models.CASCADE,
        related_name='t_fsd_next_sentence',
        null=True,
        blank=True,
    )


class Sentence(models.Model):
    _string = None

    @property
    def string(self) -> list:
        sentence_words = FeaturesWordSentence.objects.filter(sentence=self.pk).all()
        sentence_first_word = sentence_words.filter(previous_word=None).first()
        first_word = sentence_first_word.word
        self._string = ''
        self._string = f'{first_word.string}'
        next_word = sentence_first_word.next_word
        while next_word is not None:
            sentence_word = sentence_words.filter(word=next_word).first()
            word = sentence_word.word
            self._string += f' {word.string}'
            next_word = sentence_word.next_word
        return self._string


class FeaturesWordSentence(models.Model):
    sentence = models.ForeignKey(
        to='Sentence',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    previous_word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
        related_name='t_fws_previous_word',
        null=True,
        blank=True,
    )
    word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
        related_name='t_fws_word',
        null=False,
        blank=False,
    )
    next_word = models.ForeignKey(
        to='Word',
        on_delete=models.CASCADE,
        related_name='t_fws_next_word',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'word: {self.word}, sentence: {self.sentence}'


class Word(models.Model):
    string = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.string}'


class Class(models.Model):
    title = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.string}'
