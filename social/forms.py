from django import forms
from .models import Post

class PostForm(forms.ModelForm):

	# set variable equal to each form

	body = forms.CharField(
		label='', #will remove ugly label
		# tells user what actual input should be:
		widget=forms.Textarea(attrs={
			'rows': '4', #size
			'placeholder': 'Say Something...'
			}))
	class Meta:
		''' put here what you want in the form, should be based on Post model:'''
		model = Post 
		fields = ['body']
