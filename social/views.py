from django.shortcuts import render, redirect
from django.urls import reverse_lazy, re_path
## LoginRequiredMxixin, if you add it to any view, page will redirect user to log in page if they aren't logged in 
## UserPassesTestMixin, if user passes boolean expression, will allow them to view page and if not, throws 403 error. :) 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView



# Create your views here.

# use third import statement to make sure everyone is logged in to view, this is 
# passed in the () of each class. 

class PostListView(LoginRequiredMixin, View):
	
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


class PostDetailView(LoginRequiredMixin, View):
	'''takes you to a page w/ single post with all the comments listed below it'''

	# need get method to handle get requests to display page
	def get(self, request, pk, *args, **kwargs): #use pk to differentiate between different posts
		'''method to handle get requests.'''
		post = Post.objects.get(pk=pk)
		# render comment form:
		form = CommentForm()

		# copied from line 90

		comments = Comment.objects.filter(post=post).order_by('-created_on')

		# add line 67 to get request:
		context = {
			'post': post,
			'form': form,
			'comments': comments,
		}

		return render(request, 'social/post_detail.html', context)


	# need a post method to handle post requests for posting comments
	def post(self, request, pk, *args, **kwargs):
		'''so you can submit a comment'''
		post = Post.objects.get(pk=pk)
		# pass data into form
		form = CommentForm(request.POST)
		# check if form is valid:
		if form.is_valid():
			#save form
			new_comment = form.save(commit=False)
			# set author and post on object
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()

		# list comments so they are visible:
		# grab comment object and filter by which post it belongs to and order by date its created on!
		# newest first, oldest last
		comments = Comment.objects.filter(post=post).order_by('-created_on')
		# now add to post request:
		context = {
			'post': post,
			'form': form,
			'comments': comments,
		}

		return render(request, 'social/post_detail.html', context)




class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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


	def test_func(self):
		''' function for the UserPassesTestMixin, boolean expression '''

		post = self.get_object()
		# if user in request matches author, returns true and allows access to this view
		return self.request.user == post.author 


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	'''Create a view for Deleting Posts.'''

	model = Post
	template_name = 'social/post_delete.html'
	# unlike above we do not need a field, bc no form, and also we
	# do not need a function only a variable to redirect url
	success_url = reverse_lazy('post-list')

	def test_func(self):
		''' function for the UserPassesTestMixin, boolean expression '''

		post = self.get_object()
		# if user in request matches author, returns true and allows access to this view
		return self.request.user == post.author 



# create view to delete comments:

###### BUGS FIXED ! :) 

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	''' a way to delete comments '''
	model = Comment
	template_name = 'social/comment_delete.html'

	def get_success_url(self):
		''' to redirect page to post after you delete comment '''

		pk = self.kwargs['post_pk']
		return reverse_lazy('post-detail', kwargs={'pk': pk})

	def test_func(self):
		''' function for the UserPassesTestMixin, boolean expression '''

		post = self.get_object()
		# if user in request matches author, returns true and allows access to this view
		return self.request.user == post.author 

# CREATE VIEW FOR USER MODEL:

class ProfileView(View):
	''' a way to view profiles '''

	def get(self, request, pk, *args, **kwargs):
		''' to handle get requests to view profiles '''
		# we need to show all post and profile information:
		# go into list of userprofiles and get the correct profile then save as profile:
		profile = UserProfile.objects.get(pk=pk)
		user = profile.user
		# to get all the posts for the user:
		posts = Post.objects.filter(author=user).order_by('-created_on')
		# get all objects in many to many field
		followers = profile.followers.all()

		## use booleen logic to see if user is following someone to determine if 'follow' button should display

		####if no followers

		if len(followers) == 0:
			is_following = False

		for follower in followers:
			if follower == request.user:
				is_following = True
				break
			else:
				is_following = False
		# get length of list
		number_of_followers = len(followers)

		context = {
			'user': user,
			'profile': profile,
			'posts': posts,
			'number_of_followers': number_of_followers,
			#add is following to context dictionary 
			'is_following': is_following,
		}

		return render(request, 'social/profile.html', context)



class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	''' a way to edit profiles '''
	model = UserProfile
	fields = ['name', 'bio', 'birth_date', 'location', 'picture']
	template_name = 'social/profile_edit.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('profile', kwargs={'pk': pk})

	def test_func(self):
		profile = self.get_object()
		return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
	''' To handle post requests to add followers '''
	def post(self, request, pk, *args, **kwargs):
		#get profile you are on
		profile = UserProfile.objects.get(pk=pk)
		# add to followers field
		profile.followers.add(request.user)
		# return profile view to redirect
		return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
	''' to handle post requests to remove followers '''
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		# use remove to remove from follower many to many field
		profile.followers.remove(request.user)
		return redirect('profile', pk=profile.pk)

