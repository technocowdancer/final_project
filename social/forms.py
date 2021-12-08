from django import forms
from .models import Post, Comment, Reply


class PostForm(forms.ModelForm):
    '''create a form for users to submit posts.'''
    # set variable equal to each form

    body = forms.CharField(
        label='',  # will remove ugly label
        # tells user what actual input should be:
        widget=forms.Textarea(attrs={
            'rows': '4',  # size
            'placeholder': 'Say Something...'
        }))
    # to add images to form
    image = forms.ImageField(required=False)

    class Meta:
        ''' put here what you want in the form, should be based on Post model:'''
        model = Post
        fields = ['body', 'image', "tags", ]


class CommentForm(forms.ModelForm):
    '''create a form for users to create comments on posts.'''

    # very similar to post form, just need to change variables

    comment = forms.CharField(
        label='',  # will remove ugly label
        # tells user what actual input should be:
        widget=forms.Textarea(attrs={
            'rows': '4',  # size
            'placeholder': 'Post a comment...'
        }))

    class Meta:
        ''' put here what you want in the form, should be based on Comment model:'''
        model = Comment
        fields = ['comment']


class ReplyForm(forms.ModelForm):
    """create a form for users to create comments on posts."""
    # very similar to post form, just need to change variables
    reply = forms.CharField(
        label='',  # will remove ugly label
        # tells user what actual input should be:
        widget=forms.Textarea(attrs={
            'rows': '4',  # size
            'placeholder': 'Reply...'
        }))

    class Meta:
        ''' put here what you want in the form, should be based on Comment model:'''
        model = Reply
        fields = ['reply']
