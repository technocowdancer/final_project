from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy, re_path
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
## LoginRequiredMxixin, if you add it to any view, page will redirect user to log in page if they aren't logged in 
## UserPassesTestMixin, if user passes boolean expression, will allow them to view page and if not, throws 403 error. :) 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, ReplyForm
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Count
from taggit.models import Tag
from django.template.defaultfilters import slugify


# Create your views here.

# use third import statement to make sure everyone is logged in to view, this is 
# passed in the () of each class. 

class PostListView(LoginRequiredMixin, View):
    """list of all posts in social feed."""

    # get method to handle all get requests that are in this URL
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        """grab all posts, order from newest to oldest"""

        posts = Post.objects.all().order_by('-created_on').annotate(commentcount=Count('comments'))
        form = PostForm()
        common_tags = Post.tags.most_common()[:4]
        context = {
            'post_list': posts,
            'form': form,
            "users": users,
            "common_tags": common_tags
        }
        return render(request, 'social/post_list.html', context)

    # handle Post requests:

    def post(self, request, *args, **kwargs):
        users = User.objects.all()
        """to handle post requests for when user hits submit button"""
        posts = Post.objects.all().order_by('-created_on').annotate(commentcount=Count('comments'))
        form = PostForm(request.POST, request.FILES)

        # Check if form is valid:
        common_tags = Post.tags.most_common()[:4]
        if form.is_valid():
            # display in list of posts
            # set user to who is signed in
            # create variable to store new post
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.slug = slugify(new_post.body)
            new_post.save()
            form.save_m2m()

        context = {
            'post_list': posts,
            'form': form,
            "users": users,
            "common_tags": common_tags
        }
        return render(request, 'social/post_list.html', context)


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'social/post_detail.html', context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'social/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
    """takes you to a page w/ single post with all the comments listed below it"""

    # need get method to handle get requests to display page
    def get(self, request, pk, *args, **kwargs):  # use pk to differentiate between different posts
        """method to handle get requests."""
        post = Post.objects.get(pk=pk)
        # render comment form:
        form = CommentForm()
        reply_form = ReplyForm()

        # copied from line 90

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        common_tags = Post.tags.most_common()[:4]
        # add line 67 to get request:
        context = {
            'post': post,
            'form': form,
            "reply_form" : reply_form,
            'comments': comments,
            "comments_count": len(comments),
            "common_tags": common_tags,
        }

        return render(request, 'social/post_detail.html', context)

    # need a post method to handle post requests for posting comments
    def post(self, request, pk, *args, **kwargs):
        """so you can submit a comment"""
        post = Post.objects.get(pk=pk)
        # pass data into form
        form = CommentForm(request.POST)
        # check if form is valid:
        if form.is_valid():
            # save form
            new_comment = form.save(commit=False)
            # set author and post on object
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            post.comments.add(request.user)


        # list comments so they are visible:
        # grab comment object and filter by which post it belongs to and order by date its created on!
        # newest first, oldest last
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        # now add to post request:
        common_tags = Post.tags.most_common()[:4]
        context = {
            'post': post,
            'form': form,
            'comments': comments,
            "comments_count": len(comments),
            "common_tags": common_tags
        }

        return render(request, 'social/post_detail.html', context)



class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    ''' Create View for Editing Posts.'''

    model = Post
    fields = ['image', 'body']
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
            # add is following to context dictionary
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
        # get profile you are on
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


class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        # if not in field, add to many to many field, use loop

        # return list from like field
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            post.likes.add(request.user)
        # to undo like:
        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class UserSearch(View):
    '''a view to search with navbar'''

    def get(self, request, *args, **kwargs):
        '''to put parameter of search in url'''
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(Q(user__username__icontains=query))
        context = {
            'profile_list': profile_list,
        }
        return render(request, 'social/search.html', context)


class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {

            'profile': profile,
            'followers': followers,

        }

        return render(request, 'social/followers_list.html', context)


class AddReply(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        reply_form = ReplyForm(request.POST)
        comment = Comment.objects.get(pk=pk)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.author = request.user
            reply.comment = comment
            reply.save()
        next = request.POST.get('next', "/social/") #need this to be post-detail (refreshes page)
        return HttpResponseRedirect(next)

