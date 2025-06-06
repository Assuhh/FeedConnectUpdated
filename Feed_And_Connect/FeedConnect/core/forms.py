from django import forms
from .models import Product, Service, Message, SellerProfile, PaymentProof,ProductReview
from django.core.validators import RegexValidator

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']  # Ensure 'category' and 'location' are included
        
class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

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

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['display_name', 'gcash_fullname', 'gcash_number', 'gcash_qr', 'location']

    def clean_gcash_number(self):
        number = self.cleaned_data.get('gcash_number')
        if number and not str(number).isdigit():
            raise forms.ValidationError("GCash number must contain digits only.")
        return number

    def clean(self):
        cleaned_data = super().clean()
        gcash_qr = cleaned_data.get('gcash_qr')

        if not gcash_qr:
            self.add_error('gcash_qr', 'You must upload a GCash QR code before saving.')

    
class PaymentProofForm(forms.ModelForm):
    reference_number = forms.CharField(
        required=True,
        max_length=12,
        validators=[RegexValidator(r'^\d{1,12}$', message="Reference number must be 1 to 12 digits.")],
        widget=forms.TextInput(attrs={
            'required': 'required',
            'placeholder': 'Enter your payment reference number',
            'class': 'form-control',
            'maxlength': '12',
            'inputmode': 'numeric',  # mobile devices show numeric keypad
            'pattern': r'\d{1,12}',  # restrict input to digits only
            'title': 'Enter up to 12 digits only',
        }),
    )

    class Meta:
        model = PaymentProof
        fields = ['reference_number', 'screenshot']
        widgets = {
            'screenshot': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    class Meta:
        model = PaymentProof
        fields = ['reference_number', 'screenshot']
        widgets = {
            'screenshot': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_reference_number(self):
        ref = self.cleaned_data.get('reference_number')
        if ref and len(ref) > 12:
            raise forms.ValidationError("Reference number must be at most 12 characters.")
        return ref
