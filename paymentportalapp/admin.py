from django.contrib import admin

# Register your models here.
from .models import *

# =============================Custom start=======================================
# admin.site.register(Rating)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','mobileno','image',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name','customer_email','customer_project_title','status','total_cost','milestone','start_date','due_date')

