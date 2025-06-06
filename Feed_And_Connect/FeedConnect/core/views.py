from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Comment, Conversation, Message,ProductReview
from .models import FeedHistory, FeedingSchedule, Product, Service, Message, Conversation, ProductRating, PaymentProof, SellerProfile,SellerReview
from .forms import ProductForm, ServiceForm, MessageForm, PaymentProofForm, SellerProfileForm, ProductReviewForm
from django.views.decorators.http import require_POST
from itertools import chain
from django.core.paginator import Paginator
import random
import requests
import time
import calendar
import json
from datetime import timedelta
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout as django_logout
from django.db.models import Q, Max, Count, Avg
from .models import FeedHistory
from collections import defaultdict
from django.http import JsonResponse
# Create your views here.

# Blynk token and URL
BLYNK_TOKEN = 'jNOji09kF2W8YYSWkvKZF_Gdl0WsYi8x'
# Updated to use the correct Blynk HTTP API endpoint
BLYNK_URL = 'https://blynk.cloud/external/api/update'

def send_to_blynk(pin, value, retry_count=3):
    """Send a value to a Blynk virtual pin with retry logic."""
    url = f"{BLYNK_URL}?token={BLYNK_TOKEN}&{pin}={value}"
    
    for attempt in range(retry_count):
        try:
            response = requests.get(url, timeout=10)
            print(f"Attempt {attempt + 1} - Sent to Blynk {pin}={value}, Response: {response.status_code}")
            
            if response.status_code == 200:
                return True
            else:
                print(f"Blynk API returned status code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Blynk API error on attempt {attempt + 1}: {e}")
            
        # Wait before retry (except on last attempt)
        if attempt < retry_count - 1:
            time.sleep(1)
    
    return False

def send_multiple_to_blynk(pin_value_pairs, delay_between=0.5):
    """Send multiple values to Blynk with delays to avoid rate limiting."""
    results = []
    for pin, value in pin_value_pairs:
        result = send_to_blynk(pin, value)
        results.append((pin, result))
        if delay_between > 0:
            time.sleep(delay_between)
    return results

def time_to_seconds(time_str):
    """Convert HH:MM string to seconds since midnight."""
    if not time_str:
        return 0
    try:
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        return time_obj.hour * 3600 + time_obj.minute * 60
    except ValueError:
        return 0

def get_next_feeding_time(feeding_times, is_active):
    if not is_active:
        return 'Schedule OFF'

    now = datetime.now().time()
    now_seconds = now.hour * 3600 + now.minute * 60 + now.second

    # Filter out empty or invalid times and convert to seconds
    valid_times = []
    for time_str in feeding_times:
        if time_str:
            seconds = time_to_seconds(time_str)
            if seconds > 0:
                valid_times.append((seconds, time_str))

    if not valid_times:
        return 'No times set'

    valid_times.sort()

    # Find next time today
    for seconds, time_str in valid_times:
        if seconds > now_seconds:
            return time_str

    # If none left today, return first feeding time for tomorrow
    return f"{valid_times[0][1]} (Tomorrow)"


def log_scheduled_feeding(request):
    try:
        portion = int(request.GET.get('portion', 70))  # Default to 70g if not provided
        FeedHistory.objects.create(feed_type='scheduled', amount=portion)
        return JsonResponse({'status': 'success', 'message': 'Scheduled feeding logged.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def dashboard(request):
    schedule, created = FeedingSchedule.objects.get_or_create(id=1)

    error_messages = []
    success_messages = []

    if request.method == 'POST':
        # Handle portion size
        portion = request.POST.get('portion', '70')
        try:
            portion = int(portion)
            if not (10 <= portion <= 255):
                portion = 70
        except (ValueError, TypeError):
            portion = 70

        # Handle feed now (manual feed)
        if 'feed_now' in request.POST:
            print(f"Feed now requested with portion: {portion}")
            
            pin_value_pairs = [
                ('V1', portion),  # Set portion size
                ('V0', 1)         # Trigger feed
            ]
            
            results = send_multiple_to_blynk(pin_value_pairs, delay_between=1.0)
            
            if all(result[1] for result in results):
                # ✅ Save manual feeding to FeedHistory
                FeedHistory.objects.create(feed_type='manual', amount=portion)
                success_messages.append(f"Dispensed {portion} grams successfully.")
            else:
                failed_pins = [pin for pin, success in results if not success]
                error_messages.append(f"Failed to send to Blynk pins: {failed_pins}. Please try again.")

        # Handle feeding schedule update
        else:
            print("Processing schedule update...")

            feeding_times_input = []
            feeding_times_seconds = []

            for i in range(1, 5):
                time_str = request.POST.get(f'schedule_time{i}', '').strip()
                if time_str:
                    try:
                        datetime.strptime(time_str, '%H:%M')
                        feeding_times_input.append(time_str)
                        seconds = time_to_seconds(time_str)
                        feeding_times_seconds.append(seconds)
                        print(f"Feeding time {i}: {time_str} = {seconds} seconds")
                    except ValueError:
                        feeding_times_input.append(None)
                        feeding_times_seconds.append(0)
                        error_messages.append(f"Invalid time format for Feeding Time {i}.")
                else:
                    feeding_times_input.append(None)
                    feeding_times_seconds.append(0)

            schedule.feeding_time1 = feeding_times_input[0]
            schedule.feeding_time2 = feeding_times_input[1]
            schedule.feeding_time3 = feeding_times_input[2]
            schedule.feeding_time4 = feeding_times_input[3]

            is_active = request.POST.get('schedule_toggle') == '1'
            schedule.is_active = is_active
            
            print(f"Schedule active: {is_active}")
            print(f"Feeding times: {feeding_times_input}")

            schedule.save()

            pin_value_pairs = [
                ('V4', 1 if is_active else 0),
                ('V7', feeding_times_seconds[0]),
                ('V8', feeding_times_seconds[1]),
                ('V9', feeding_times_seconds[2]),
                ('V10', feeding_times_seconds[3]),
            ]

            print(f"Sending to Blynk: {pin_value_pairs}")

            results = send_multiple_to_blynk(pin_value_pairs, delay_between=1.0)

            failed_pins = [pin for pin, success in results if not success]
            if failed_pins:
                error_messages.append(f"Failed to update device pins: {failed_pins}")
            else:
                success_messages.append("Schedule updated successfully on device.")

    # Prepare dashboard context
    feeding_times = [
        schedule.feeding_time1 or '',
        schedule.feeding_time2 or '',
        schedule.feeding_time3 or '',
        schedule.feeding_time4 or '',
    ]

    active_count = sum(1 for t in feeding_times if t)
    last_feed = FeedHistory.objects.filter(feed_type='manual').order_by('-timestamp').first()
    last_portion = last_feed.amount if last_feed else 70
    next_feeding_time = get_next_feeding_time(feeding_times, schedule.is_active)

    context = {
        'feeding_times': feeding_times,
        'schedule_active': schedule.is_active,
        'last_portion': last_portion,
        'schedule_count': active_count,
        'next_feeding_time': next_feeding_time,
    }

    for msg in success_messages:
        messages.success(request, msg)
    for msg in error_messages:
        messages.error(request, msg)

    return render(request, 'dashboard.html', context)

def feed_history(request):
    feed_history = FeedHistory.objects.all().order_by('-timestamp')
    return render(request, 'feed_history.html', {'feed_history': feed_history})


@csrf_exempt
def dashboard_1(request):
    schedule, created = FeedingSchedule.objects.get_or_create(id=1)

    error_messages = []
    success_messages = []

    if request.method == 'POST':
        portion = request.POST.get('portion', '50')
        try:
            portion = int(portion)
            if not (10 <= portion <= 500):
                portion = 50
        except (ValueError, TypeError):
            portion = 50

        if 'feed_now' in request.POST:
            print(f"Feed now requested with portion: {portion}")

            pin_value_pairs = [
                ('V1', portion),
                ('V0', 1)
            ]

            results = send_multiple_to_blynk(pin_value_pairs, delay_between=1.0)

            if all(result[1] for result in results):
                FeedHistory.objects.create(feed_type='manual', amount=portion)
                success_messages.append(f"Dispensed {portion} grams successfully.")
            else:
                failed_pins = [pin for pin, success in results if not success]
                error_messages.append(f"Failed to send to Blynk pins: {failed_pins}. Please try again.")
        else:
            print("Processing schedule update...")

            feeding_times_input = []
            feeding_times_seconds = []

            for i in range(1, 5):
                time_str = request.POST.get(f'schedule_time{i}', '').strip()
                if time_str:
                    try:
                        datetime.strptime(time_str, '%H:%M')
                        feeding_times_input.append(time_str)
                        seconds = time_to_seconds(time_str)
                        feeding_times_seconds.append(seconds)
                        print(f"Feeding time {i}: {time_str} = {seconds} seconds")
                    except ValueError:
                        feeding_times_input.append(None)
                        feeding_times_seconds.append(0)
                        error_messages.append(f"Invalid time format for Feeding Time {i}.")
                else:
                    feeding_times_input.append(None)
                    feeding_times_seconds.append(0)

            schedule.feeding_time1 = feeding_times_input[0]
            schedule.feeding_time2 = feeding_times_input[1]
            schedule.feeding_time3 = feeding_times_input[2]
            schedule.feeding_time4 = feeding_times_input[3]

            is_active = request.POST.get('schedule_toggle') == '1'
            schedule.is_active = is_active

            print(f"Schedule active: {is_active}")
            print(f"Feeding times: {feeding_times_input}")

            schedule.save()

            pin_value_pairs = [
                ('V4', 1 if is_active else 0),
                ('V7', feeding_times_seconds[0]),
                ('V8', feeding_times_seconds[1]),
                ('V9', feeding_times_seconds[2]),
                ('V10', feeding_times_seconds[3]),
            ]

            print(f"Sending to Blynk: {pin_value_pairs}")

            results = send_multiple_to_blynk(pin_value_pairs, delay_between=1.0)

            failed_pins = [pin for pin, success in results if not success]
            if failed_pins:
                error_messages.append(f"Failed to update device pins: {failed_pins}")
            else:
                success_messages.append("Schedule updated successfully on device.")

    feeding_times = [
        schedule.feeding_time1 or '',
        schedule.feeding_time2 or '',
        schedule.feeding_time3 or '',
        schedule.feeding_time4 or '',
    ]

    active_count = sum(1 for t in feeding_times if t)
    last_feed = FeedHistory.objects.filter(feed_type='manual').order_by('-timestamp').first()
    last_portion = last_feed.amount if last_feed else 70

    # Convert next feeding time string(s) to datetime.time objects for 12-hour display
    def get_next_feeding_time_obj(feeding_times, is_active):
        if not is_active:
            return None

        now = datetime.now().time()
        future_times = []

        for t in feeding_times:
            if t:
                try:
                    parsed_time = datetime.strptime(t, '%H:%M').time()
                    if parsed_time > now:
                        future_times.append(parsed_time)
                except ValueError:
                    continue

        if future_times:
            return min(future_times)
        else:
            valid_times = []
            for t in feeding_times:
                if t:
                    try:
                        valid_times.append(datetime.strptime(t, '%H:%M').time())
                    except ValueError:
                        continue
            return min(valid_times) if valid_times else None

    next_feeding_time = get_next_feeding_time_obj(feeding_times, schedule.is_active)

    context = {
        'feeding_times': feeding_times,
        'schedule_active': schedule.is_active,
        'last_portion': last_portion,
        'schedule_count': active_count,
        'next_feeding_time': next_feeding_time,  # This is a datetime.time object now
    }

    for msg in success_messages:
        messages.success(request, msg)
    for msg in error_messages:
        messages.error(request, msg)

    return render(request, 'dashboard_1.html', context)

def feed_history1(request):
    feed_history = FeedHistory.objects.all().order_by('-timestamp')
    
    # Optional: Filtering by range (last 7 or 30 days)
    range_days = request.GET.get('range')
    if range_days and range_days.isdigit():
        days = int(range_days)
        cutoff_date = datetime.now() - timedelta(days=days)
        feed_history = feed_history.filter(timestamp__gte=cutoff_date)
    
    # Optional: Filtering by month
    month = request.GET.get('month')
    if month and month.isdigit():
        month_num = int(month)
        feed_history = feed_history.filter(timestamp__month=month_num)
    
    # Paginate feed_history, 12 items per page
    paginator = Paginator(feed_history, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    month_choices = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    context = {
        'feed_history': page_obj,  # pass page_obj for pagination in template
        'page_obj': page_obj,
        'month_choices': month_choices,
    }
    
    return render(request, 'feed_history1.html', context)

@csrf_exempt
def record_scheduled_feed(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = int(data.get('amount', 0))
            FeedHistory.objects.create(
                amount=amount,
                feed_type='scheduled'
            )
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.seller != request.user:
        return redirect('marketplace')  # Block unauthorized edits

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('marketplace')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})

def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if service.seller != request.user:
        return redirect('marketplace')  # Block unauthorized edits

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)

    return render(request, 'edit_service.html', {'form': form})

#NEW#
@login_required(login_url='signin')
def seller_profile(request, seller_id=None):
    # If no seller_id or it's the logged-in user's ID, show/edit own profile
    if seller_id is None or int(seller_id) == request.user.id:
        profile, created = SellerProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            form = SellerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('seller_profile', seller_id=request.user.id)
        else:
            form = SellerProfileForm(instance=profile)

        return render(request, 'seller_profile.html', {
            'profile_user': request.user,
            'profile': profile,
            'form': form,
            'is_own_profile': True,
        })

    # Otherwise, show another user's profile in read-only mode
    seller_user = get_object_or_404(User, id=seller_id)
    profile = get_object_or_404(SellerProfile, user=seller_user)
    listings = Product.objects.filter(seller=seller_user)
    reviews = SellerReview.objects.filter(seller=seller_user)

    return render(request, 'seller_profile.html', {
        'profile_user': seller_user,
        'profile': profile,
        'listings': listings,
        'reviews': reviews,
        'is_own_profile': False,
    })
    
@login_required(login_url='signin')   
def payment_success(request):
    return render(request, 'payment_success.html')


@login_required(login_url='signin')
def buy_now(request, item_type, item_id):
    if item_type != 'product':
        messages.error(request, "Invalid item type.")
        return redirect('marketplace')

    product = get_object_or_404(Product, id=item_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('product_detail', pk=item_id)

        if quantity < 1 or quantity > product.stock:
            messages.error(request, "Invalid quantity.")
            return redirect('product_detail', pk=item_id)

        total_price = product.price * quantity

        # Save order info to session for payment page use
        request.session['order'] = {
            'product_id': product.id,
            'quantity': quantity,
            'total_price': float(total_price),
        }

        # Redirect to payment page WITHOUT product_id in URL
        return redirect('payment')

    # if GET, redirect to product detail page
    return redirect('product_detail', pk=item_id)

@login_required(login_url='signin')
def payment(request):
    order = request.session.get('order')
    if not order:
        messages.error(request, "No order found. Please start your purchase again.")
        return redirect('marketplace')

    # Retrieve product and order info
    product = get_object_or_404(Product, pk=order['product_id'])
    seller_profile = getattr(product.seller, 'sellerprofile', None)
    quantity = order.get('quantity', 1)
    total_price = order.get('total_price', product.price)

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            payment_proof = form.save(commit=False)

            # **Correctly assign the real model fields:**
            payment_proof.buyer = request.user
            payment_proof.seller = product.seller
            payment_proof.item_type = 'product'
            payment_proof.item_id = product.id
            # (Optional) store quantity/price on the proof if you extend the model
            payment_proof.quantity = quantity
            payment_proof.total_price = total_price

            payment_proof.save()

            # Clear the saved order
            del request.session['order']

            return redirect('payment_success')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PaymentProofForm()

    return render(request, 'payment.html', {
        'product': product,
        'seller_profile': seller_profile,
        'form': form,
        'quantity': quantity,
        'total_price': total_price,
    })


@login_required(login_url='signin')   
def seller_payments(request):
    # Only show payments where current user is the seller
    payments = PaymentProof.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'seller_payments.html', {'payments': payments})

@login_required(login_url='signin')
@require_POST
def confirm_payment(request, payment_id):
    payment = get_object_or_404(PaymentProof, id=payment_id)

    if request.user != payment.seller:
        return HttpResponseForbidden("You are not allowed to confirm this payment.")

    # Mark payment as confirmed
    payment.is_confirmed = True
    payment.confirmed_at = timezone.now()
    payment.save()

    # Reduce product stock
    product = get_object_or_404(Product, id=payment.item_id)
    if product.stock >= payment.quantity:
        product.stock -= payment.quantity
        product.save()
    else:
        # Optional: Handle overselling case
        return HttpResponseForbidden("Not enough stock to confirm this payment.")

    # Get or create conversation
    conversations = (
        Conversation.objects.annotate(num_participants=Count("participants"))
        .filter(participants=payment.buyer)
        .filter(participants=payment.seller)
        .filter(num_participants=2)
    )

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(payment.buyer, payment.seller)

    # Attach product to conversation
    conversation.products.add(product)

    # Send confirmation message
    Message.objects.create(
        sender=payment.seller,
        receiver=payment.buyer,
        content=f"Hi! Your payment for '{product.name}' has been confirmed. Thank you for your purchase!",
        conversation=conversation,
        product=product,
    )

    # Redirect back to inbox so seller sees latest message
    return redirect('inbox')

@login_required(login_url='signin')
def payment_confirmations(request):
    # Show only unconfirmed payments where the current user is the seller
    pending = PaymentProof.objects.filter(seller=request.user, is_confirmed=False)
    return render(request, 'payment_confirmations.html', {'payments': pending})

@login_required(login_url='signin')
def my_payments(request):
    payments = PaymentProof.objects.filter(buyer=request.user).order_by('-created_at')
    
    enriched_payments = []
    for payment in payments:
        item = None
        if payment.item_type == 'product':
            item = Product.objects.filter(id=payment.item_id).first()
        elif payment.item_type == 'service':
            item = Service.objects.filter(id=payment.item_id).first()

        # Fix zero total price for old data
        if payment.total_price == 0 and item:
            payment.total_price = item.price * payment.quantity

        enriched_payments.append({
            'payment': payment,
            'item': item
        })

    return render(request, 'my_payments.html', {'enriched_payments': enriched_payments})

#Marketplace
@login_required(login_url='signin')
def marketplace(request):
    query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'date')
    category_filter = request.GET.get('category', '')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_filter:
        products = products.filter(category__iexact=category_filter)
    if sort_option == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    # Annotate products with average rating and review count
    products = products.annotate(avg_rating=Avg('reviews__rating')).annotate(review_count=Avg('reviews__id'))

    # Attach seller profiles and precompute avg_rating_int
    seller_ids = products.values_list('seller_id', flat=True).distinct()
    seller_profiles = SellerProfile.objects.filter(user_id__in=seller_ids)
    profiles_dict = {profile.user_id: profile for profile in seller_profiles}

    for product in products:
        product.seller_profile = profiles_dict.get(product.seller_id)
        product.avg_rating_int = int(round(product.avg_rating or 0))

    # Categories combined for filters
    product_categories = dict(Product.CATEGORY_CHOICES)
    service_categories = dict(Service.CATEGORY_CHOICES)
    combined_categories = {**product_categories, **service_categories}

    services = Service.objects.all()
    if query:
        services = services.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_filter:
        services = services.filter(category__iexact=category_filter)
    if sort_option == 'name':
        services = services.order_by('name')
    else:
        services = services.order_by('-created_at')

    stars = range(1, 6)

    return render(request, 'marketplace.html', {
        'products': products,
        'services': services,
        'query': query,
        'selected_category': category_filter,
        'sort_option': sort_option,
        'categories': combined_categories,
        'stars': stars,
    })

@login_required
def rate_product(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 0))

        # Allow users to rate any product, even their own
        if 1 <= rating <= 5:
            ProductRating.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'rating': rating}
            )

    return redirect('marketplace')


@login_required(login_url='signin')
def post_item(request):
    # Always define these so they exist
    product_form = ProductForm()
    service_form = ServiceForm()

    if request.method == 'POST':
        item_type = request.POST.get('item_type')

        if item_type == 'product':
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.seller = request.user

                # Add seller location from SellerProfile
                try:
                    product.location = request.user.sellerprofile.location
                except SellerProfile.DoesNotExist:
                    product.location = ''  # fallback if no seller profile

                product.save()
                return redirect('marketplace')

        elif item_type == 'service':
            service_form = ServiceForm(request.POST, request.FILES)
            if service_form.is_valid():
                service = service_form.save(commit=False)
                service.seller = request.user
                service.save()
                return redirect('marketplace')

    return render(request, 'post_item.html', {
        'product_form': product_form,
        'service_form': service_form
    })

from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def my_listings(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    services = Service.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'my_listings.html', {
        'products': products,
        'services': services,
    })

#Messaging 
# 🔁 Helper function to get or create a conversation between exactly two users
@login_required(login_url='signin')
def inbox(request):
    from django.db.models import Q

    # Get messages involving the current user
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(conversation__participants=request.user)
    ).order_by('-timestamp')

    seen_conversations = set()
    latest_messages = []

    for msg in messages:
        if msg.conversation_id not in seen_conversations:
            # Only mark as unread if the current user is the receiver
            msg.is_unread = (msg.receiver == request.user and not getattr(msg, 'read', False))
            latest_messages.append(msg)
            seen_conversations.add(msg.conversation_id)

    return render(request, 'inbox.html', {
        'latest_messages': latest_messages,
        'current_conversation_id': None,
    })


@login_required(login_url='signin')
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Ensure the user is part of the conversation
    if request.user not in conversation.participants.all():
        return redirect('inbox')

    # ✅ Mark all unread messages sent *to the user* as read
    conversation.messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    messages = conversation.messages.all().order_by('timestamp')
    form = MessageForm()

    # Handle the form submission for new messages
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            receiver = conversation.get_other_users(request.user).first()
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                conversation=conversation,
                timestamp=timezone.now()
            )
            return redirect('conversation_detail', conversation_id=conversation_id)

    # Handle inquired product or service
    inquired_item_url = None
    inquired_item_id = None
    if conversation.products.exists():
        inquired_item_url = 'product_detail'
        inquired_item_id = conversation.products.first().id
    elif conversation.services.exists():
        inquired_item_url = 'service_detail'
        inquired_item_id = conversation.services.first().id

    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'inquired_item_url': inquired_item_url,
        'inquired_item_id': inquired_item_id,
    }
    return render(request, 'conversation_detail.html', context)

@login_required(login_url='signin')
def send_message(request, receiver_id, item_type, item_id):
    sender = request.user
    receiver = get_object_or_404(User, id=receiver_id)

    # Validate item (product or service)
    item = None
    product = None
    service = None

    if item_type == 'product':
        product = get_object_or_404(Product, id=item_id)
        item = product
    elif item_type == 'service':
        service = get_object_or_404(Service, id=item_id)
        item = service
    else:
        messages.error(request, 'Invalid item type specified.')
        return redirect('inbox')

    # Look for an existing conversation between sender and receiver based on product or service inquiry
    conversation = (
        Conversation.objects
        .filter(participants=sender)
        .filter(participants=receiver)
        .filter(
            Q(products=product) | Q(services=service)
        )
        .distinct()
        .first()
    )

    if not conversation:
        # Create a new conversation if none exists
        conversation = Conversation.objects.create()
        conversation.participants.set([sender, receiver])
        # Associate the product or service with the conversation if applicable
        if product:
            conversation.products.add(product)
        elif service:
            conversation.services.add(service)
        conversation.save()

    # Handle message sending
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                conversation=conversation,
            )
            return redirect('conversation_detail', conversation_id=conversation.id)

    return render(request, 'send_message.html', {
        'conversation': conversation,
        'item': item,
        'item_type': item_type,
        'receiver': receiver,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    buy_now_mode = request.GET.get('buy_now') == '1'

    # Only fetch reviews if not in buy_now mode
    if not buy_now_mode:
        reviews = product.reviews.all().order_by('-created_at')
        average_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    else:
        reviews = []
        average_rating = None

    if request.method == 'POST' and 'submit_review' in request.POST:
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.id)
    else:
        review_form = ProductReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1) if average_rating else None,
        'review_form': review_form,
        'buy_now_mode': buy_now_mode,
    }
    return render(request, 'product_detail.html', context)

@login_required(login_url='signin')
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'servicedetail.html', {'service': service})



from django.db.models import Q
from itertools import chain
import random

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # Get list of usernames the current user is following
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    user_following_list = [user.user for user in user_following]

    # Include current user's username in the list
    user_following_list.append(request.user.username)

    # Get posts from followed users and self
    feed = Post.objects.filter(user__in=user_following_list).order_by('-created_at')

    # Suggestions logic (unchanged)
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {
        'user_profile': user_profile,
        'posts': feed,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4]
    })

@csrf_exempt
def delete_product(request, index):
    if 'products' in request.session:
        products = request.session['products']
        if 0 <= index < len(products):
            del products[index]
            request.session['products'] = products
    return redirect('marketplace')

@csrf_exempt
def delete_service(request, index):
    if 'services' in request.session:
        services = request.session['services']
        if 0 <= index < len(services):
            del services[index]
            request.session['services'] = services
    return redirect('marketplace')

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption', '')

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('index')
    else:
        return redirect('index')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('index')

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')
    user_post_length = user_posts.count()

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = FollowersCount.objects.filter(user=pk)
    user_following = FollowersCount.objects.filter(follower=pk)

    # Get actual User objects from FollowersCount
    followers_list = [User.objects.get(username=f.follower) for f in user_followers]
    following_list = [User.objects.get(username=f.user) for f in user_following]

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers.count(),
        'user_following': user_following.count(),
        'followers_list': followers_list,
        'following_list': following_list,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def get_followers(request, username):
    followers_qs = FollowersCount.objects.filter(user=username)
    followers = []
    for f in followers_qs:
        try:
            user_obj = User.objects.get(username=f.follower)
            followers.append({
                'username': user_obj.username,
                'profile_url': f'/profile/{user_obj.username}',  # example link to profile
            })
        except User.DoesNotExist:
            continue
    return JsonResponse({'followers': followers})

@login_required(login_url='signin')
def get_following(request, username):
    following_qs = FollowersCount.objects.filter(follower=username)
    following = []
    for f in following_qs:
        try:
            user_obj = User.objects.get(username=f.user)
            following.append({
                'username': user_obj.username,
                'profile_url': f'/profile/{user_obj.username}',
            })
        except User.DoesNotExist:
            continue
    return JsonResponse({'following': following})


def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("comment")
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image') or user_profile.profileimg
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        first_time = not user_profile.profile_complete  # Check if first time setup

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.profile_complete = True  # Mark as complete
        user_profile.save()

        if first_time:
            return redirect('main page')  # Redirect only once after setup
        else:
            return redirect('index')  # Stay on settings after future edits

    return render(request, 'setting.html', {'user_profile': user_profile})
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Log user in  and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')
    
@login_required(login_url='signin')
def main_page(request):
    return render(request, 'dashboard.html')
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main page')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


def landing_page(request):
    return render(request, 'landing page.html')

def landing_2(request):
    return render(request, 'landing2.html')

def feed(request):
    return render(request, 'feed.html')
