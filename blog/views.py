from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import F
from hitcount.views import HitCountDetailView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <appp>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <appp>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(HitCountDetailView):
    model = Post
    count_hit = True

    #self.visit = statute.visits
    # return super().get(request, *args, **kwargs)

    #pk1 = Post.pk
    #Post.objects.filter(pk=2).update(visit=F('visit') + 1)

    # def get(self, request, *args, **kwargs):
    ##post = get_object_or_404(Post, pk=kwargs['pk'])

    # def test_func(self):
    #post = self.get_object()
    #pk1 = get_object_or_404(Post, model=self.kwargs.get('pk'))
    #Post.objects.filter(pk=post.id).update(visit=F('visit') + 1)
    # return True

    # def get_queryset(self):
    #   pk1 = get_object_or_404(Post, model=self.kwargs.get('pk'))
    #   Post.objects.filter(pk=pk1).update(visit=F('visit') + 1)
    #   pk1 = get_object_or_404(Post, pk=self.kwargs.get('pk'))
    #  Post.objects.filter(pk=pk1).update(visit=F('visit') + 1)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
    return render(request, "blog/about.html", {"title": "About"})