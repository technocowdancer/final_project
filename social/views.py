from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import Post
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView


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


class PostDetailView(View):
	'''takes you to a page w/ single post with all the comments listed below it'''

	# need get method to handle get requests to display page
	def get(self, request, pk, *args, **kwargs): #use pk to differentiate between different posts
		'''method to handle get requests.'''
		post = Post.objects.get(pk=pk)
		# render comment form:
		form = CommentForm()
		context = {
			'post': post,
			'form': form,
		}

		return render(request, 'social/post_detail.html', context)


	# need a post method to handle post requests for posting comments


class PostEditView(UpdateView):
	''' Create View for Editing Posts.'''

	model = Post
	fields = ['body']
	template_name = 'social/post_edit.html'

	# to tell program where to redirect after you're done:
	def get_success_url(self):
		'''redirect url'''
		# get the pk
		pk = self.kwargs['pk']

		# redirect url
		return reverse_lazy('post-detail', kwargs={'pk': pk})



