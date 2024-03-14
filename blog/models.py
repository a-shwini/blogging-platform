from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage



class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    blog_post_limit = models.IntegerField()
    active = models.BooleanField(default=True)
    features = models.TextField()

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def get_image_upload_path(instance, filename):
        return 'images/' + filename

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Category.get_image_upload_path, storage=FileSystemStorage(location='blog/static/image/4.jpg'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    subscription_required = models.BooleanField(default=True)

def __str__(self):
        return self.title
