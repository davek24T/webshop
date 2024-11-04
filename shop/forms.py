from django import forms
import random
import string
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Product

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, label="Register as")
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha = forms.CharField(label='Enter the text shown below', max_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate a random CAPTCHA string
        self.captcha_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'captcha')

    def clean_captcha(self):
        captcha_input = self.cleaned_data.get('captcha')
        if captcha_input != self.captcha_value:
            raise forms.ValidationError("Incorrect CAPTCHA. Please try again.")
        return captcha_input

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        
class RequestToBuyForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Message', required=False)
    
