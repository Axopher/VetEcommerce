from django import forms
from .models import ShippingAddress

class BillingForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Just start typing your address here...'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    
    class Meta:
        model = ShippingAddress
        fields = ['address','country','state','city','pin_code','latitude','longitude']
        exclude = ['customer','order']

        widgets = {
            'country': forms.TextInput(attrs={
                'title': 'Please enter address powered by Google.',
                'required': 'required',
                'class':'automatic_field',

            }),
            'state': forms.TextInput(attrs={
                'required': 'required',
                'title': 'Please enter address powered by Google.',
                'class':'automatic_field',

            }),
            'city': forms.TextInput(attrs={
                'required': 'required',
                'title': 'Please enter address powered by Google.',
                'class':'automatic_field',
            }),
            'pin_code': forms.TextInput(attrs={
                'title': 'Please enter address powered by Google',
                'class':'automatic_field',
            }),
            }        

    # to set latitude and longitude as readonly field
    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field == 'latitude' or field == 'longitude':
    #             self.fields[field].widget.attrs.['readonly'] = 'readonly'
