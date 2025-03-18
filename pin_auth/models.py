from django.db import models

# Create your models here.
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    name = models.CharField(max_length=100)
    pin_hash = models.CharField(max_length=128)  
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_pin(self, pin):
        self.pin_hash = make_password(pin)
        
    def check_pin(self, pin):
        return check_password(pin, self.pin_hash)
    
    def __str__(self):
        return self.name