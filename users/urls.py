from django.urls import path
from . import views
from .views import ProfileCreateView, ProfileUpdateView

urlpatterns = [
	path('accounts/<str:slug>/profile/', views.profile, name='profile'),
	path('accounts/profile/create/', ProfileCreateView.as_view(), name='create-profile'),
	path('accounts/profile/<str:slug>/update/', ProfileUpdateView.as_view(), name='update-profile'),
	path('accounts/profile/<str:slug>/followers/', views.followers, name='followers'),
	path('accounts/profile/<str:slug>/followings/', views.followings, name='followings'),
]