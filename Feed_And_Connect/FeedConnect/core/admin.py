from django.contrib import admin
from .models import (
    Profile,
    Post,
    LikePost,
    FollowersCount,
    Order,
    FeedingSchedule,
    FeedingLog,
    FeedHistory,
    SellerProfile,
    PaymentProof,
    SellerReview,
    Product,
    ProductRating,
    Service,
    Message,
    Conversation,
    Comment,
    ProductReview,
)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Order)
admin.site.register(FeedingSchedule)
admin.site.register(FeedingLog)
admin.site.register(FeedHistory)
admin.site.register(SellerProfile)
admin.site.register(PaymentProof)
admin.site.register(SellerReview)
admin.site.register(Product)
admin.site.register(ProductRating)
admin.site.register(Service)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(Comment)
admin.site.register(ProductReview)