from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView
)

from .forms import PostForm, CommentForm, ProfileEditForm
from .models import Post, Category, User
from core.constants import POST_MAX_LENGTH
from core.mixins import AuthorCheckMixin, CommentMixin, PostMixin
from core.utils import (
    annotate_posts_with_comment_count,
    filter_posts_by_date_and_publication
)


class IndexListView(ListView):
    model = Post
    paginate_by = POST_MAX_LENGTH
    template_name = 'blog/index.html'
    queryset = annotate_posts_with_comment_count(
        filter_posts_by_date_and_publication(Post.objects)
    )


class PostDetailView(ListView):
    model = Post
    template_name = 'blog/detail.html'
    pk_field = 'post_id'
    pk_url_kwarg = 'post_id'
    paginate_by = POST_MAX_LENGTH

    def get_queryset(self):
        return self.get_object().comments.select_related('author')

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs[self.pk_url_kwarg])
        if self.request.user != post.author and (
            post.pub_date > timezone.now() or not post.is_published
        ):
            raise Http404
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = self.get_object().comments.all()
        return context


class CategoryPostsListView(ListView):
    paginate_by = POST_MAX_LENGTH
    template_name = 'blog/category.html'

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return annotate_posts_with_comment_count(
            filter_posts_by_date_and_publication(self.get_category().posts)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(PostMixin, UpdateView):
    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(PostMixin, DeleteView):
    pass


class ProfileListView(ListView):
    paginate_by = POST_MAX_LENGTH
    template_name = 'blog/profile.html'

    def get_profile(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        profile = self.get_profile()
        posts = annotate_posts_with_comment_count(profile.posts)
        if self.request.user != profile:
            posts = filter_posts_by_date_and_publication(posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'profile': self.get_profile()})
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/user.html'
    form_class = ProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=[self.request.user])


class CommentCreateView(CommentMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(AuthorCheckMixin, CommentMixin, UpdateView):
    pass


class CommentDeleteView(AuthorCheckMixin, CommentMixin, DeleteView):
    pass


class RegistrationCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('blog:profile',
                           kwargs={'username': self.request.user.username})
        else:
            return reverse('blog:index')
