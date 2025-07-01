from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import get_followers, get_following
from .views import record_scheduled_feed

urlpatterns = [
    path('', views.signin, name='signin'),
    path('index', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    # path('profile/', views.landing_page, name='landing page'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup/', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('dashboard1/', views.dashboard_1, name='main page'),
    path('landing_2', views.landing_2, name='landing page'),
    # path('feed', views.feed, name='feed'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('BMI/', views.feed_history, name= 'BMI'),

    path('record-scheduled-feed/', record_scheduled_feed, name='record_scheduled_feed'),

    path('dashboard1/', views.dashboard_1, name='dashboard_1'),
    path('history1/', views.feed_history1, name= 'feed_history1'),
    path('main_page', views.main_page, name='maine page'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('seller-profile/', views.seller_profile, name='my_seller_profile'),
    path('seller-profile/<int:seller_id>/', views.seller_profile, name='seller_profile'),

    path('my-payments/', views.my_payments, name='my_payments'),
    path('buy-now/<str:item_type>/<int:item_id>/', views.buy_now, name='buy_now'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-confirmations/', views.payment_confirmations, name='payment_confirmations'),
    path('payment-confirmations/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
    path('payment/', views.payment, name='payment'),


    # Messaging
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    # path('message/product/<int:receiver_id>/<int:product_id>/', views.send_message_product, name='send_message_product'),
    # path('message/service/<int:receiver_id>/<int:service_id>/', views.send_message_service, name='send_message_service'),
    path('message/<int:receiver_id>/<str:item_type>/<int:item_id>/', views.send_message, name='send_message'),
    # Post Product/Service
    path('post/', views.post_item, name='post_item'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('service/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('message/<int:receiver_id>/<int:service_id>/', views.send_message, name='send_message'),
    path('delete-product/<int:index>/', views.delete_product, name='delete_product'),
    path('delete-service/<int:index>/', views.delete_service, name='delete_service'),
    path('profile/<str:username>/followers/', get_followers, name='get_followers'),
    path('profile/<str:username>/following/', get_following, name='get_following'),
    path('product/<int:product_id>/rate/', views.rate_product, name='rate_product'),
    path('comment/<uuid:post_id>/', views.add_comment, name='add_comment'),

]

