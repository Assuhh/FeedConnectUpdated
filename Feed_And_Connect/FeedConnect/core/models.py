from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from datetime import datetime

from django.utils.timezone import now

User = get_user_model()

class FeedingSchedule(models.Model):
    
    feeding_time1 = models.CharField(max_length=5, blank=True, null=True)
    feeding_time2 = models.CharField(max_length=5, blank=True, null=True)
    feeding_time3 = models.CharField(max_length=5, blank=True, null=True)
    feeding_time4 = models.CharField(max_length=5, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    portion = models.PositiveIntegerField(default=50)


    def __str__(self):
        return f"Schedule {self.id} - {'Active' if self.is_active else 'Inactive'}"

class FeedingLog(models.Model):
    pet_name = models.CharField(max_length=100, default='')
    timestamp = models.DateTimeField(default=now)
    portion_dispensed = models.FloatField(default=0.0)
    success = models.BooleanField(default=True)

class FeedHistory(models.Model):
    
    FEED_TYPE_CHOICES = (
        ('manual', 'Manual'),
        ('scheduled', 'Scheduled'),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()  # Amount of food dispensed
    feed_type = models.CharField(max_length=10, choices=FEED_TYPE_CHOICES)

    def __str__(self):
        return f"{self.timestamp} - {self.feed_type} - {self.amount}g"
    
    class Meta:
        ordering = ['-timestamp']

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    gcash_fullname = models.CharField(max_length=100, blank=True)
    gcash_number = models.CharField(max_length=20, blank=True, null=True)
    gcash_qr = models.ImageField(upload_to='gcash_qr_codes/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)  # <-- New field

    def __str__(self):
        return self.display_name or self.user.username
    
    
class PaymentProof(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_proofs')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_payments')
    item_type = models.CharField(max_length=20)  # "product" or "service"
    item_id = models.PositiveIntegerField()
    reference_number = models.IntegerField(blank=True, null=True)
    screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment from {self.buyer.username} to {self.seller.username} for {self.item_type} #{self.item_id}"

class SellerReview(models.Model):
    reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='received_reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'seller')

    def __str__(self):
        return f"{self.reviewer} rated {self.seller} - {self.rating}/5"

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    payment = models.OneToOneField('PaymentProof', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.product.title} from {self.seller.username} to {self.buyer.username}"

class Product(models.Model):
    STATUS_CHOICES = [
        ('selling', 'Selling'),
        ('sold', 'Sold'),
    ]

    CATEGORY_CHOICES = [
        ('toys', 'Toys'),
        ('food', 'Food'),
        ('accessories', 'Accessories'),
        ('other', 'Other'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='selling')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)#new#
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    # color_options = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)


    # @property
    # def has_colors(self):
    #     return bool(self.color_options)
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #unique_together = ('product', 'user')  # one review per product per user
        pass
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

class ProductRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product')


       
# class SellerReview(models.Model):
#     reviewer = models.ForeignKey(User, related_name='given_reviews', on_delete=models.CASCADE)
#     seller = models.ForeignKey(User, related_name='received_reviews', on_delete=models.CASCADE)
#     rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     comment = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('reviewer', 'seller')

#     def str(self):
#         return f"{self.reviewer} rated {self.seller} - {self.rating}/5"

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('grooming', 'Grooming'),
        ('training', 'Training'),
        ('walking', 'Walking'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # ← Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey('Conversation', related_name='messages', on_delete=models.CASCADE, default=1)
    is_read = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    
    # Optional references
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.sender} to {self.receiver} at {self.timestamp}"

class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    products = models.ManyToManyField(Product, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

    def get_involved_items(self):
        # Combine all the products and services in the conversation
        return self.products.all() | self.services.all()

    @property
    def involved_item(self):
        # You can modify this method to return the first product/service as a general reference
        if self.products.exists():
            return self.products.first()
        if self.services.exists():
            return self.services.first()
        return None

    def get_other_users(self, user):
        # Return all participants except the one passed in (the current user)
        return self.participants.exclude(id=user.id)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture-973460_1280.png')
    location = models.CharField(max_length=100, blank=True)
    profile_complete = models.BooleanField(default=False)  # <-- Add this field

    def __str__(self):
        return self.user.username
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Link to Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who made the comment
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
