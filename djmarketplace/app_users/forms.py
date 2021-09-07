from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from django.utils.translation import gettext_lazy as _


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False, label=_('date of birth'),
                                    widget=SelectDateWidget(years=range(datetime.now().year, 1910, -1)))
    city = forms.CharField(max_length=30, label=_('city'))
    phone_number = forms.CharField(max_length=15, label=_('phone number'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, label=_('title'))
    description = forms.CharField(max_length=50, label=_('description'))
    file = forms.FileField()


class UserForm(forms.ModelForm):
    date_of_birth = forms.DateField(required=False, label=_('date of birth'),
                                    widget=SelectDateWidget(years=range(datetime.now().year, 1920, -1)))
    city = forms.CharField(max_length=30, label=_('city'))
    phone_number = forms.CharField(max_length=15, label=_('phone number'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()


class AddBalanceForm(forms.Form):
    quantity = forms.DecimalField(max_digits=20, decimal_places=2, label=_('Quantity'))


class BoughtItemsReportFilter(forms.Form):
    first_date = forms.DateField(required=False, label=_('from'),
                                 widget=SelectDateWidget(years=range(datetime.now().year, 2020, -1)))
    second_date = forms.DateField(required=False, label=_('to'),
                                 widget=SelectDateWidget(years=range(datetime.now().year, 2020, -1)))
