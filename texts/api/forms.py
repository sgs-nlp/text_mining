from django import forms


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
