from django import forms
from .models import Product, Service, Message, SellerProfile, PaymentProof

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']  # Ensure 'category' and 'location' are included

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
        fields = ['display_name','gcash_fullname','gcash_number', 'gcash_qr', 'location']

    def clean_gcash_number(self):
        number = self.cleaned_data.get('gcash_number')
        if number and not number.isdigit():
            raise forms.ValidationError("GCash number must contain digits only.")
        return number
    
class PaymentProofForm(forms.ModelForm):
    reference_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'required': 'required',
            'placeholder': 'Enter your payment reference number',
            'class': 'form-control',
        })
    )

    class Meta:
        model = PaymentProof
        fields = ['screenshot', 'reference_number']  # include screenshot here

        widgets = {
            'screenshot': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    class Meta:
        model = PaymentProof
        fields = ['reference_number', 'screenshot']
        widgets = {
            'screenshot': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
