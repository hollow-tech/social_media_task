
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PostSerializer

from .models import Post

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
	'List':'',
	'Detail View':'post/<int:pk>/',
	'Create':'post-create/',
	'Update':'post-update/<int:pk>/',
	'Delete':'post-delete/<int:pk>/',
	}
	return Response(api_urls)

@api_view(['GET'])
def postList(request):
	posts = Post.objects.all()
	serializer = PostSerializer(posts, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def postDetail(request, pk):
	posts = Post.objects.get(id=pk)
	serializer = PostSerializer(posts, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def postCreate(request):
	serializer = PostSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['POST'])
def postUpdate(request, pk):
	post = Post.objects.get(id=pk)
	serializer = PostSerializer(instance=post, data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)

@api_view(['DELETE'])
def postDelete(request, pk):
	post = Post.objects.get(id=pk)
	post.delete()
	return Response("Post has been deleted!")

# ========================================================================
class CustomLoginView(LoginView):
	template_name = 'base/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('posts')

class RegisterPage(FormView):
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('posts')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(RegisterPage, self).form_valid(form)

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('posts')
		return super(RegisterPage, self).get(*args, **kwargs)


class PostList(LoginRequiredMixin, ListView):
	model = Post
	context_object_name = 'posts'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["posts"] = context['posts'].filter(user=self.request.user)

		search_input = self.request.GET.get('search-area') or ''
		if search_input:
			context['posts'] = context['posts'].filter(title__startswith=search_input)

		context['search_input'] = search_input
		return context
	
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class PostDetail(LoginRequiredMixin, DetailView):
	model = Post
	context_object_name = 'post'
	template_name = 'base/post.html'


class PostCreate(LoginRequiredMixin, CreateView):
	model=Post
	fields = ['title', 'text']
	success_url = reverse_lazy('posts')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(PostCreate, self).form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
	model = Post
	fields = ['title', 'text']
	success_url = reverse_lazy('posts')

class PostDelete(LoginRequiredMixin, DeleteView):
	model = Post
	context_object_name = 'post'
	success_url = reverse_lazy('posts')