from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Post, Comment, Reply, Like
from .forms import CommentForm, ReplyForm
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from users.models import Connections


def index(request):
    posts = Post.objects.all().order_by('-created')[:3]
    return render(request, 'posts/index.html', {'posts':posts})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'
    ordering = ['-created']


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'image', 'content', 'choice1', 'choice2']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):

    def get(self, request, *args, **kwargs):

        try:
            post = Post.objects.get(slug=kwargs['slug'])
        except Post.DoesNotExist:
            return redirect('404')

        if Connections.objects.filter(follower__username=request.user, following=post.author).exists():
        	follows = True
        else:
        	follows = False

        if Like.objects.filter(user=request.user, post=post).exists():
        	like=True
        else:
        	like = False

        likes = Like.objects.filter(post=post)

        return render(request, 'posts/post_detail.html', {'post':post, 'follows': follows, 'like': like, 'likes': likes})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image', 'content', 'choice1', 'choice2']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):

    def get(self, request, *args, **kwargs):
        ruser = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = Post.objects.all().filter(author=ruser)
        return render(request, 'posts/user_posts.html', {'posts':posts, 'ruser':ruser})


def comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = request.POST.get('content')
            comment = Comment.objects.create(post=post, author=request.user, content=comment)
            comment.save()
            comment_form=CommentForm()

    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'posts/comments.html', context)


def replytocomment(request, slug, id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=id)
    replies = Reply.objects.filter(comment=comment).order_by('-id')

    if request.method == 'POST':
        reply_form = ReplyForm(request.POST or None)
        if reply_form.is_valid():
            reply = request.POST.get('content')
            reply = Reply.objects.create(comment=comment, author=request.user, content=reply)
            reply.save()
            reply_form=ReplyForm()

    else:
        reply_form = ReplyForm()

    context = {
        'post': post,
        'comment': comment,
        'replies': replies,
        'reply_form': reply_form,
    }
    print(comment)

    return render(request, 'posts/replies.html', context)


@login_required
def follow(request, *args, **kwargs):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(username=kwargs['username'])

    if follower == following:
        messages.warning(request, 'You cannot follow yourself.')

    else:
        connection = Connections.objects.get_or_create(follower=follower, following=following)

        if connection:
            messages.success(request, 'You\'ve successfully followed {}.'.format(following.username))
        else:
            messages.warning(request, 'You\'ve already followed {}.'.format(following.username))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request, *args, **kwargs):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(username=kwargs['username'])

    if follower == following:
        messages.warning(request, 'You cannot follow yourself.')

    else:
        connection = Connections.objects.get(follower=follower, following=following)

        connection.delete()

        messages.success(request, 'You\'ve unfollwed {}.'.format(following.username))

    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def like(request, *args, **kwargs):
    post = Post.objects.get(slug=kwargs['slug'])
    like = Like.objects.get_or_create(post=post, user=request.user)

    if like:
        messages.success(request, 'You\'ve liked the post.')
        return HttpResponseRedirect(reverse('post-detail', kwargs= {'slug':post.slug}))
        # return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.warning(request, 'You\'ve already liked the post.')
        return HttpResponseRedirect(reverse('post-detail', kwargs= {'slug':post}))


@login_required
def dislike(request, *args, **kwargs):
    like = Like.objects.get(post__slug=kwargs['slug'], user=request.user)
    print(like)

    like.delete()

    messages.success(request, 'You\'ve disliked the post.')

    return redirect(request.META.get('HTTP_REFERER'))


def error404(request):
    return render(request, 'main/404.html')


def Form(request):
    return render(request, "posts/uploads.html", {})

def Upload(request):
    for count, x in enumerate(request.FILES.getlist("files")):
        def process(f):
            with open('/home/nitesh2/Codes/Projects/Django/myProjects/blogs/media/files/' + str(count), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        process(x)
    return HttpResponse("File(s) uploaded!")
