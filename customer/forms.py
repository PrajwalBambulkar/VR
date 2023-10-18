from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# class CustomerRegistration(UserCreationForm):
#     password1 = forms.CharField(label='Password',widget=forms.PasswordInput(),label_suffix='')
#     password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(),label_suffix='')
#     email = forms.CharField(required=True ,widget=forms.EmailInput(),label_suffix='',label='Email / Mobile no.')
#     username = forms.CharField(required=True ,widget=forms.TextInput(),label_suffix='',help_text='*')


#     class Meta:
#         model = User
#         label  = {'email': 'Email Address'}
#         fields = ['username','email','password1','password2']

# class CustomerRegistration(UserCreationForm):
#     password1 = forms.CharField(label='Password',widget=forms.PasswordInput(),label_suffix='')
#     password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(),label_suffix='')
#     email = forms.CharField(required=True ,widget=forms.EmailInput(),label_suffix='',)
#     mobile = forms.IntegerField(label='Mobile')
#     username = forms.CharField(required=True ,widget=forms.TextInput(),label_suffix='',help_text='*')


#     class Meta:
#         model = User
#         label  = {'email': 'Email Address','mobile': 'Mobile'}
#         fields = ['username','email','mobile','password1','password2']


class CustomerRegistration(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), label_suffix='')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), label_suffix='')
    email = forms.CharField(required=True, widget=forms.EmailInput(), label_suffix='')
    mobile = forms.IntegerField(label='Mobile No', label_suffix='')
    username = forms.CharField(required=True, widget=forms.TextInput(), label_suffix='', help_text='*')

    class Meta:
        model = User
        label = {'email': 'Email Address', 'mobile': 'Mobile No', 'password1': 'Password', 'password2': 'Confirm Password'}
        fields = ['username', 'email', 'mobile', 'password1', 'password2']

        

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))  # yaha hum true k bad , lgaker css k class add kr skte hai 
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Seller

# class SellerRegistration(UserCreationForm):
#     email = forms.CharField(required=True, widget=forms.EmailInput(), label_suffix='', label='Email')
#     username = forms.CharField(required=True, widget=forms.TextInput(), label_suffix='', help_text='*')
#     mobile_no = forms.CharField(required=True, label='Mobile Number', widget=forms.TextInput(), label_suffix='')
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), label_suffix='')
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), label_suffix='')

#     # Add seller-specific fields
#     company_name = forms.CharField(required=True, label='Company Name', widget=forms.TextInput(), label_suffix='')
#     company_address = forms.CharField(required=True, label='Company Address', widget=forms.TextInput(), label_suffix='')

#     class Meta:
#         model = User
#         labels = {'email': 'Email Address'}
#         fields = ['username', 'email', 'mobile_no', 'company_name', 'company_address', 'password1', 'password2']



from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SellerRegistration(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput(), label_suffix='', label='Email')
    username = forms.CharField(required=True, widget=forms.TextInput(), label_suffix='', help_text='*')
    mobile_no = forms.CharField(required=True, label='Mobile Number', widget=forms.TextInput(), label_suffix='')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), label_suffix='')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), label_suffix='')

    # Add seller-specific fields
    company_name = forms.CharField(required=True, label='Company Name', widget=forms.TextInput(), label_suffix='')
    company_address = forms.CharField(required=True, label='Company Address', widget=forms.TextInput(), label_suffix='')

    class Meta:
        model = User
        labels = {'email': 'Email Address'}
        fields = ['username', 'email', 'mobile_no', 'company_name', 'company_address', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match. Please enter matching passwords.")

        return cleaned_data



class SellerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(), label='Username', label_suffix='')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', label_suffix='')



from django import forms
from .models import Seller

class SellerFilterForm(forms.Form):
    seller = forms.ModelChoiceField(
        queryset=Seller.objects.filter(is_seller=True),
        empty_label="Select Seller",
        required=False,
        to_field_name='seller'  # Set the field to display in the dropdown
    )


#change pass
from django.contrib.auth.forms import PasswordChangeForm
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User 



from .models import Seller  # Import the Seller model

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['company_name', 'company_address', 'mobile_no']