from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'Full name'}),
                   required=True
                   )
    shipping_email = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'Email'}),
                   required=True
                   )
    shipping_address1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'Address1'}),
                   required=True
                   
    )
    shipping_address2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'Address2'}),
                   required=False
                   
    )
    shipping_city = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'City'}),
                   required=True
    )
    shipping_state = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'State'}),
                   required=False
    )
    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'ZipCode'}),
                   required=False
                   )
    shipping_country = forms.CharField(
        label="",
        widget=forms.PasswordInput(
        attrs={'class':'form-control',
                   'name':'password',
                   'type':'password',
                   'placeholder':'country'}),
                   required=True
                   )
    
    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_email',
            'shipping_address1',
            'shipping_address2',
            'shipping_city',
            'shipping_state',
            'shipping_zipcode',
            'shipping_country',
        ]
        exclude = ['user',]