from django import forms
from .models import List, Review, TreatBrands, Comment, Reply
from django.forms import ModelForm, TextInput, Textarea



GENRE_CHOICES = (
    ("", ""),
    ('メンズ', 'メンズ'),
    ('ウィメンズ', 'ウィメンズ'),
    ('メンズ・ウィメンズ', 'メンズ・ウィメンズ'),
)
TREAT_USED_CHOICES = (
    ("", ""),
    ('有','有'),
    ('無','無'),
)

class ListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = List
        fields = ["shopname", "treatbrand", "treat_brand", "treatused", "genre", "address", "hpurl" ]

class SearchForm(forms.Form):
    shopname = forms.CharField(
        initial='',
        label='ショップ名',
        required = False, # 必須ではない
    )
    treatbrand = forms.CharField(
        initial='',
        label='取扱ブランド',
        required=False,  # 必須ではない
    )
    treatused = forms.fields.ChoiceField(
        choices=TREAT_USED_CHOICES,
        initial='',
        label='古着の取扱',
        required=False,  # 必須ではない
    )
    genre = forms.fields.ChoiceField(
        choices=GENRE_CHOICES,
        initial='',
        label='ジャンル',
        required=False,  # 必須ではない
    )
    address = forms.CharField(
        initial='',
        label='所在地',
        required=False,  # 必須ではない
    )
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review','author')
        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'コメント内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ('author', 'text')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': '名前',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': '返信内容',
            }),
        }
        labels = {
            'author': '',
            'text': '',
        }

