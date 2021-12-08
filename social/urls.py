from django.urls import path
from .views import (PostListView, PostDetailView, PostEditView, CommentDeleteView, ProfileView, ProfileEditView,
                    PostDeleteView, AddFollower, RemoveFollower, AddLike, UserSearch, ListFollowers,detail_view,
                    tagged,AddReply)

# ProfileDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/comment/reply/<int:pk>', AddReply.as_view(), name='comment-reply'),
    path('post/edit/<int:pk>', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/followers/', ListFollowers.as_view(), name='list-followers'),
    # path('profile/delete/<int:pk>', ProfileDeleteView.as_view(), name='profile-delete'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('search/', UserSearch.as_view(), name="profile-search"),
    path('post/<slug:slug>/', detail_view, name="detail"),
    path('tag/<slug:slug>/', tagged, name="tagged"),
]
