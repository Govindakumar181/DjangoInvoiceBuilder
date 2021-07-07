from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
                # ForeignKey
    mobileno = models.IntegerField(default='00000000000')
    image = models.ImageField(upload_to='media/',default='profile.jpg')
    
    def __str__(self):
        return self.user.username+" profile "

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def update_profile(sender,instance,created,**kwargs):
    if created == False:
        instance.profile.save()

STATUS_CHOICES = (
   ('Unpaid', 'Unpaid'),
   ('Paid', 'Paid'),
   ('Partial Paid', 'Partially Paid')
)
class Customer(models.Model):
    customer_name = models.CharField(default=' ',max_length=200)
    customer_email = models.CharField(default=' ',max_length=200)
    customer_project_title = models.CharField(default=' ',max_length=200)
    status = models.CharField(choices=STATUS_CHOICES,default='Unpaid', max_length=128)
    total_cost = models.IntegerField(default='00')
    milestone = models.IntegerField(default='00')
    # customer_project = models.TextField()
    start_date = models.DateTimeField(default=datetime.now(), blank=True)
    due_date = models.DateTimeField(default=datetime.now(), blank=True)
    
    def __str__(self):
        return self.customer_name
