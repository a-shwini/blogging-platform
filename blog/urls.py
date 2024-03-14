from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PostViewSet, SubscriptionPlanViewSet, SubscriptionViewSet
from .views import create_post_api
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('accounts/home/', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.filter_posts, name='filter_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('api/create_post/', create_post_api, name='create_post_api'),
    
]



router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'subscription-plans', SubscriptionPlanViewSet)
router.register(r'user-subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]