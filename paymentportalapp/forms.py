from django import forms
from django.forms import ModelForm
from .models import *

class formCustomer(forms.ModelForm):
  class Meta:
      model= Customer
      fields= ["customer_name", "customer_email", "customer_project_title","status","total_cost","milestone","start_date","due_date",]