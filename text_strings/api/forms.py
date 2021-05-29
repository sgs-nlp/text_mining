from django import forms


class Word2DBInput(forms.Form):
    word = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )
    pos_tagging = forms.CharField(
        required=False,
        max_length=32,
        min_length=1,
    )


class Word2DBOutput(forms.Form):
    id = forms.CharField(
        required=True,
        max_length=32,
        min_length=1,
    )


class Sentences2DBInput(forms.Form):
    pass


class Sentences2DBOutput(forms.Form):
    pass


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
    pass


class Documents2DBOutput(forms.Form):
    pass


class Keywords2DBInput(forms.Form):
    pass


class Keywords2DBOutput(forms.Form):
    pass


class KeywordsInput(forms.Form):
    pass


class KeywordsOutput(forms.Form):
    pass


class IsKeywordsInput(forms.Form):
    pass


class IsKeywordsOutput(forms.Form):
    pass


class Stopwords2DBInput(forms.Form):
    pass


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
