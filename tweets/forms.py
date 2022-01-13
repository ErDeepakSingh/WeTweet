from django import forms
from .models import Tweet

class TweetCreationForm(forms.ModelForm):
    message=forms.CharField(required=True,label='Make a Tweet', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    class Meta:
        model=Tweet
        fields=('message',)