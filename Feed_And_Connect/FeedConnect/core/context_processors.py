# yourapp/context_processors.py
from .models import Message
from django.db.models import Q
from .models import PaymentProof

def unread_message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
    else:
        count = 0
    return {'unread_count': count}

def payment_confirmation_count(request):
    if request.user.is_authenticated:
        count = PaymentProof.objects.filter(seller=request.user, is_confirmed=False).count()
        return {'pending_count': count}
    return {'pending_count': 0}