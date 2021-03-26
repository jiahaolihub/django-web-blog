from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    LikeView,
    AddCommentView,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # need to pass username variable
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # need to pass an integer
    path('like/<int:pk>/', LikeView, name='like_post'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # need to pass an integer
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # need to pass an integer
    path('about/', views.about, name='blog-about'),
]
