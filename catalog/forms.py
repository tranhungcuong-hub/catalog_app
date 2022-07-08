from django import forms
from django.contrib.auth.models import User
from mptt.forms import TreeNodeChoiceField
from .models import Post, Category

categories = Category.objects.all().values_list('name', 'name')


class CateForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['parent'].widget.attrs.update(
        #     {'class': 'd-none'})
        # self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Category
        fields = ['name', 'parent']


class PostForm(forms.ModelForm):
    user = User
    images = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': True
    }))
    print(categories)
    category = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                         choices=categories)

    class Meta:
        model = Post
        fields = ('title', 'author', 'thumnail', 'script')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'thumnail': forms.ClearableFileInput(attrs={"class": "form-control"}),
            'script': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'elder', 'type': 'hidden'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'script', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'script': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=categories, attrs={'class': 'form-control'}),
        }
