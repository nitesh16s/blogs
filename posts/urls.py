from django.urls import path
from . import views
from .views import PostListView, PostCreateView, PostUpdateView, PostDetailView, UserPostListView

urlpatterns = [
	path('', views.index, name='index'),
	path('posts/', PostListView.as_view(), name='posts'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<str:slug>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<str:slug>/', PostDetailView.as_view(), name='post-detail'),
	path('post/<str:slug>/comment/', views.comment, name='comment'),
	path('post/<str:slug>/<int:id>/reply/', views.replytocomment, name='replytocomment'),
	path('post/<str:username>/posts/', UserPostListView.as_view(), name='user-posts'),
	path('post/<str:username>/follow/', views.follow, name='follow'),
	path('post/<str:username>/unfollow/', views.unfollow, name='unfollow'),
	path('post/<str:slug>/like/', views.like, name='like'),
	path('post/<str:slug>/dislike/', views.dislike, name='dislike'),
	path('page-not-found/', views.error404, name='404'),
	path('form/', views.Form, name='form'),
	path('upload/', views.Upload, name='upload'),
]