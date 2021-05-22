from django.contrib import admin
from .models import *


@admin.register(Corpus)
class CorpusModelAdmin(admin.ModelAdmin):
    pass


@admin.register(FeaturesDocumentCorpus)
class FeaturesDocumentCorpusModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(FeaturesSentenceDocument)
class FeaturesSentenceDocumentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Sentence)
class SentenceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(FeaturesWordSentence)
class FeaturesWordSentenceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Word)
class WordModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Class)
class ClassModelAdmin(admin.ModelAdmin):
    pass
