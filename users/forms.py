from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from store.models import ShippingAddress
from .models import Customer
from django.contrib.auth.forms import PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    # def  __init__(self, *args, **kwargs):
    #     super(CustomUserCreationForm, self).__init__(*args, *kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({'class':'input'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']

        widgets = {
            'email': forms.EmailInput(attrs={
                'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'title': 'Please enter a valid email address.',
                'required': 'required',

            }),
            'first_name': forms.TextInput(attrs={
                'pattern': "[a-zA-Z\s]+",
                'title': 'Only letters and spaces are allowed.',
                'required': 'required',

            }),
            'last_name': forms.TextInput(attrs={
                'pattern': "[a-zA-Z\s]+",
                'title': 'Only letters and spaces are allowed.',
                'required': 'required',

            }),
            'phone': forms.TextInput(attrs={
                'pattern': "9[78][0-9]{8}",
                'title': 'Please enter a valid phone number.',
                'required': 'required',

            }),
            }    


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add your desired CSS class to the form fields
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter Your Old Password'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter Your New Password'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Your New password'
