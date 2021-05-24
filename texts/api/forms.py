from django import forms
import json


class DocumentInput(forms.Form):
    document = forms.CharField(
        required=False,
        max_length=2048,
    )
    document_path = forms.CharField(
        required=False,
        max_length=512,
    )


class DocumentOutput(forms.Form):
    normal_document_path = forms.BooleanField(
        required=False,
        initial=True,
    )
    sentence_tokenize = forms.BooleanField(
        required=False,
        initial=True,
    )
    word_tokenize = forms.BooleanField(
        required=False,
        initial=True,
    )
    stop_words_list = forms.BooleanField(
        required=False,
        initial=True,
    )
    key_words_list = forms.BooleanField(
        required=False,
        initial=True,
    )
    normal_document = forms.BooleanField(
        required=False,
        initial=True,
    )
    save_to_file = forms.BooleanField(
        required=False,
        initial=True,
    )
