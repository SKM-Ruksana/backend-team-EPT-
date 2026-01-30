from django.db import models

# Create your models here.
from django.db import models
import random
from django.utils import timezone

def generate_unique_code():
    return random.randint(100000, 999999)  # 6-digit OTP

class Employee_login(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    domain = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=128,default="employee")
    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.emp_id)


class verification_table(models.Model):
    emp_id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    generated_code = models.IntegerField(unique=True,default=generate_unique_code)
    created_time = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):

        return str(self.email)
