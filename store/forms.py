from django import forms
from .models import ShippingAddress

class BillingForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing...'}))
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    
    class Meta:
        model = ShippingAddress
        fields = ['address','country','state','city','pin_code','latitude','longitude']
        exclude = ['customer','order']


    # to set latitude and longitude as readonly field
    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field == 'latitude' or field == 'longitude':
    #             self.fields[field].widget.attrs.['readonly'] = 'readonly'
