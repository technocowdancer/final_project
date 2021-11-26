from django.shortcuts import render
from django.views import View
from .models import Post
from .forms import PostForm

# Create your views here.

class PostListView(View):
	
	'''list of all posts in social feed.'''

	# get method to handle all get requests that are in this URL

	def get(self, request, *args, **kwargs):
		'''grab all posts, order from newest to oldest'''
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm()
		context = {
			'post_list': posts,
			'form': form,
		}

		return render(request, 'social/post_list.html', context)

	# handle Post requests:

	def post(self, request, *args, **kwargs):
		'''to handle post requests for when user hits submit button'''
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm(request.POST)

		#Check if form is valid:

		if form.is_valid():
			#display in list of posts
			#set user to who is signed in
			# create variable to store new post
			new_post = form.save(commit=False)
			new_post.author = request.user 
			new_post.save()

		context = {
		'post_list': posts,
		'form': form,
		}

		return render(request, 'social/post_list.html', context)

pass
class PostDetailView(View):
	''''''
