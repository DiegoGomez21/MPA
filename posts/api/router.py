from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.api.views import PostApiView, CreatePostApiView, DetailPostApiView, EditPostApiView, DeletePostApiView



urlpatterns = [
    path('posts/', PostApiView.as_view(), name='posts-list'),
    path('post_create/', CreatePostApiView.as_view(), name='post_create'),
    path('post_detail/<int:pk>/', DetailPostApiView.as_view(), name='post_detail'),
    path('post_edit/<int:pk>/', EditPostApiView.as_view(), name='post_edit'),
    path('post_delete/<int:pk>/', DeletePostApiView.as_view(), name='post_delete'),
]


