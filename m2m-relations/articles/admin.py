from django.contrib import admin

from django.core.exceptions import ValidationError

from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        i = 0
        for form in self.forms:
            dictionary = form.cleaned_data
            if dictionary.get('is_main'):
                i += 1
            else:
                continue
        if i == 0:
            raise ValidationError('Выберите главную тему')
        elif i > 1:
            raise ValidationError('Главной темой может быть только одна')
        return super().clean()


class TagsTitleInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [TagsTitleInline,]
    pass

@admin.register(Tag)
class Tagadmin(admin.ModelAdmin):
    pass