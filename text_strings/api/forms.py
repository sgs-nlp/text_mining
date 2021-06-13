from django import forms


class Word2DBInput(forms.Form):
    word = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )


class Word2DBOutput(forms.Form):
    id = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )
    public_key = forms.CharField(
        required=True,
        max_length=512,
        min_length=1,
    )
    type = forms.CharField(
        required=True,
        max_length=128,
        min_length=1,
    )


class Sentences2DBInput(forms.Form):
    sentence = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )


class Sentences2DBOutput(forms.Form):
    id = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )
    public_key = forms.CharField(
        required=True,
        max_length=512,
        min_length=1,
    )
    type = forms.CharField(
        required=True,
        max_length=128,
        min_length=1,
    )


class Index2DBInput(forms.Form):
    pass


class Index2DBOutput(forms.Form):
    pass


class IndexInput(forms.Form):
    pass


class IndexOutput(forms.Form):
    pass


class IsIndexInput(forms.Form):
    pass


class IsIndexOutput(forms.Form):
    pass


class Documents2DBInput(forms.Form):
    document = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )


class Documents2DBOutput(forms.Form):
    id = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )
    public_key = forms.CharField(
        required=True,
        max_length=512,
        min_length=1,
    )
    type = forms.CharField(
        required=True,
        max_length=128,
        min_length=1,
    )


class Keywords2DBInput(forms.Form):
    document_id = forms.CharField(
        required=True,
        min_length=1,
    )
    word = forms.CharField(
        required=True,
        min_length=1,
    )


class Keywords2DBOutput(forms.Form):
    pass


class KeywordsInput(forms.Form):
    document_id = forms.CharField(
        required=True,
        min_length=1,
    )


class KeywordsExtractorInput(forms.Form):
    document = forms.CharField(
        required=True,
        min_length=1,
    )


class IsKeywordsInput(forms.Form):
    user_id = forms.CharField(
        required=True,
        max_length=512,
        min_length=1,
    )
    keywords_score_list = forms.JSONField(
        required=True,
    )


class IsKeywordsOutput(forms.Form):
    pass


class Corpus2DBInput(forms.Form):
    corpus_path = forms.CharField(
        required=True,
        min_length=1,
    )


class Corpus2DBOutput(forms.Form):
    id = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )
    public_key = forms.CharField(
        required=True,
        max_length=512,
        min_length=1,
    )
    type = forms.CharField(
        required=True,
        max_length=128,
        min_length=1,
    )


class Stopwords2DBInput(forms.Form):
    corpus_id = forms.CharField(
        required=True,
        min_length=1,
        max_length=128,
    )
    stopword_list = forms.JSONField(
        required=True,
    )


class Stopwords2DBOutput(forms.Form):
    pass


class StopwordsInput(forms.Form):
    pass


class StopwordsOutput(forms.Form):
    pass


class IsStopwordsInput(forms.Form):
    pass


class IsStopwordsOutput(forms.Form):
    pass


class NormalizeInput(forms.Form):
    pass


class NormalizeOutput(forms.Form):
    pass


class TokenizeInput(forms.Form):
    pass


class TokenizeOutput(forms.Form):
    pass


class DocumentInput(forms.Form):
    document_path = forms.CharField(
        required=False,
        max_length=512,
    )
    document = forms.CharField(
        required=False,
        max_length=2048,
    )


class DocumentOutput(forms.Form):
    normal_document_path = forms.BooleanField(
        required=False,
    )
    normal_document = forms.BooleanField(
        required=False,
    )
    sentence_tokenize = forms.BooleanField(
        required=False,
    )
    word_tokenize = forms.BooleanField(
        required=False,
    )
    stop_words_list = forms.BooleanField(
        required=False,
    )
    key_words_list = forms.BooleanField(
        required=False,
    )
    save_to_file = forms.BooleanField(
        required=False,
    )
