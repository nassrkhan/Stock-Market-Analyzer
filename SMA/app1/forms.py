from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

##############################

# from django.forms.widgets import NumberInput
# from django import forms
# import numpy as np


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




# choice=tickers.symbol    
# STOCK_CHOICES= [tuple([x,x]) for x in choice]
# FIRST_CHOICES= [('', 'Select'),]
# STOCK_CHOICES= FIRST_CHOICES + STOCK_CHOICES
 
# class Stock_List(forms.Form):
 
#     stock = forms.ChoiceField(label='Select the Stock', choices=STOCK_CHOICES,required=True, widget=forms.Select(attrs={'style': 'border-color:darkgoldenrod; border-radius: 10px;'}))
 
#     s_date = forms.DateField(label='Start Date',required=True,widget = NumberInput(attrs={'type':'date', 'style': 'border-color:darkgoldenrod; border-radius: 10px;','min': '2018-01-01' ,'max': '2018-12-31'}))
 
#     e_date = forms.DateField(label='Start Date',required=True,widget = NumberInput(attrs={'type':'date', 'style': 'border-color:darkgoldenrod; border-radius: 10px;','min': '2018-01-01' ,'max': '2018-12-31'}))