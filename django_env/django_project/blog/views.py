from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin, # checking log in session in class function, however login decorator only can be used in function.
    UserPassesTestMixin, # checking whether current user is post author or not. Mixin that allows you to define a test function which must return True
                        # if the current user can access the view.
    RedirectToPreviousMixin # record previous session, then redirect to previous page
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # will looking for path: <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # the default context name is posts_list. but change it friendly same as 'posts' that was created on database.
                                  # More: https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-display/#making-friendly-template-contexts
    ordering = ['-date_posted'] # changing posted posts ordering as recent posts.

    # Pagination
    paginate_by = 5
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # will looking for path: <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # the default context name is posts_list. but change it friendly same as 'posts' that was created on database.
                                  # More: https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-display/#making-friendly-template-contexts
    ordering = ['-date_posted'] # changing posted posts ordering as recent posts.

    # Pagination
    paginate_by = 5

    # View user all posts by clicking username.
    # get username string, and pass it to get_object; if not found user, return 404;
    # if found, return user all posts.
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    # template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['total_likes'] = likes_connected.total_likes()
        data['post_is_liked'] = liked
        return data

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # redirect to post detail page by get_absolute_url function in Post models

class AddCommentView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = Comment
    template_name = 'blog/post_comment.html'
    fields = ['name', 'content']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    # redirct to current post detail page by RedirectToPreviousMixin class which will remeber previous visited session, and then back to previous page.

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})