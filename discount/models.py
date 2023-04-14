from django.db import models
from django.contrib.auth.models import User

class Code(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    list_product = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Discount Codes"
        ordering = ['user_id', 'code', 'list_product', 'created_date']



class Status(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    connected_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return "Account "+self.user.username