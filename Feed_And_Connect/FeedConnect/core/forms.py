from django import forms
from .models import Product, Service, Message, Product, Service

class ProductForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('selling', 'Selling'),
        ('sold', 'Sold'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select, required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category', 'status']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'image', 'category']  # Ensure 'category' is included
        
class MessageForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='')
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }

