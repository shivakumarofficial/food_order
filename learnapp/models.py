from django.db import models
from django.contrib.auth.models import User


user_type = [
   ("VENDOR","Vendor"),
   ("USER","User")
]



# Create your models here.

class UserDetails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # additional fields
    phone = models.BigIntegerField()
    address =models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    userpic = models.ImageField(upload_to='userimg/',blank=True,null=True)
    user_type = models.CharField(max_length=100,choices=user_type,default="USER")





