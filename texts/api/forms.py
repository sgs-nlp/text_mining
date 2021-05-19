from django import forms
import json


class DocumentInput(forms.Form):
    document_path = forms.CharField(
        max_length=512,
        required=True,
    )

    output_fields = forms.JSONField(
        required=True,
    )
