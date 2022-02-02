from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

def home(request):
    context = {
        "posts" : Post.objects.all()
    }
    return render(request, "Blog/home.html", context)

class PostListView(ListView):
    model = Post
    template_name = "Blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_of_post"]
    paginate_by = 4

class PostDetailView(DetailView):
    model = Post                         # template_name = <app>/<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user    # set the author to the current user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:   # to check the current logged in user is the author
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserPostListView(ListView):
    model = Post
    template_name = "Blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by("-date_of_post")

def about(request):
    return render(request, "Blog/about.html", { "title" : "About" })
