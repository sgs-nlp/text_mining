from django.contrib import admin
from .models import *


@admin.register(Corpus)
class CorpusModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Document)
class DocumentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Paragraph)
class ParagraphModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Sentence)
class SentenceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(KeyWord)
class KeyWordModelAdmin(admin.ModelAdmin):
    pass


@admin.register(StopWord)
class StopWordModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Word)
class WordModelAdmin(admin.ModelAdmin):
    pass
