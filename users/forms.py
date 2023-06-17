from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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

