from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Category, Post

admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Category)
admin.site.register(Post)
