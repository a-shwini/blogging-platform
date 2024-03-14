from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, SubscriptionPlan, Subscription, Category, Post
from .serializers import PostSerializer, CategorySerializer, SubscriptionPlanSerializer, SubscriptionSerializer
from django.contrib.auth import authenticate, login
from rest_framework import viewsets,filters
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import permissions, status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PostSerializer
from .forms import PostForm
from rest_framework.renderers import TemplateHTMLRenderer
import requests
'''
def home(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    if request.GET.get('category'):
        posts = posts.filter(category__name=request.GET.get('category'))
    if request.GET.get('search'):
        posts = posts.filter(title__icontains=request.GET.get('search'))
    return render(request, 'blog/home.html', {'posts': posts, 'categories': categories})
'''
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
'''
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
'''
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user has a subscription plan
            if not user.subscription:
                # If not, assign a free subscription plan
                subscription_plan = SubscriptionPlan.objects.get(name='Free')
                Subscription.objects.create(user=user, plan=subscription_plan)
            return redirect('home')
        else:
            # Handle invalid login attempts here
            pass
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    logout(request)
    return redirect('login')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.subscription = request.user.subscription
            post.save()
             
            # API endpoint URL for creating a post
            url = 'http://127.0.0.1:8000/api/create_post/'
           
            # Data for the new post
            data = {
                'title': post.title,
                'content': post.content,
                'author': post.author.id,
                'image': post.image,
                'category': post.category.id,
            }
            # Send POST request to create a new post
            response = requests.post(url, data=data)

            return redirect('home')

    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            '''
            post = form.save(commit=False)
            post.author = request.user
            '''
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def home(request):
    posts =  Post.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'posts': posts, 'categories': categories})

@login_required
def filter_posts(request, category_id):
    category = Category.objects.get(id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'home.html', {'posts': posts, 'category': category})

@login_required
def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.all()  # Define posts with all posts initially

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    return render(request, 'home.html', {'posts': posts, 'query': query})
@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def create_post_api(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        # Handle GET request logic here
        # Return a Response object with data and specify a template name
        data = {'message': 'GET request processed successfully'}
        return Response(data, template_name='home.html')
'''
def create_post_api(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # Assign the current user as the author of the post
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
'''
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
   @permission_classes([permissions.IsAuthenticated, HasSubscriptionPlan])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)'''
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    @permission_classes([IsAuthenticated, SubscriptionPlan])
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

#hassubcriptionplan
class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


'''
class HasSubscriptionPlan(permissions.BasePermission):
    def has_permission(self, request, view):
        user_subscription = request.user.user_subscription
        return request.user.user_subscription.subscription_plan.name == 'Your Subscription Plan Name'
'''