from django.db import models


class Corpus(models.Model):
    # todo id : create id by word id hashing
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
    # todo id : create id by word id hashing
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
    # todo id : create id by word id hashing
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


def word2db(value: str) -> Word:
    wrd = Word.objects.filter(string=value).first()
    if wrd is not None:
        return wrd
    from repository.converter import to_hash
    wrd = Word()
    wrd.pk = to_hash([value])
    wrd.string = value
    wrd.save()
    return wrd


def sentence2db(value: list) -> Sentence:
    sent_id = to_hash(value)
    snt = Sentence.objects.filter(pk=sent_id).first()
    if snt is not None:
        return snt
    words = value
    snt = Sentence()
    snt.pk = sent_id
    snt.save()
    f_w_s = FeaturesWordSentence()
    f_w_s.sentence = snt
    f_w_s.previous_word = None
    f_w_s.word = word2db(words[0])
    f_w_s.next_word = word2db(words[1])
    f_w_s.save()
    for i in range(len(words) - 2):
        f_w_s = FeaturesWordSentence()
        f_w_s.sentence = snt
        f_w_s.previous_word = word2db(words[i])
        f_w_s.word = word2db(words[i + 1])
        f_w_s.next_word = word2db(words[i + 2])
        f_w_s.save()
    return snt
