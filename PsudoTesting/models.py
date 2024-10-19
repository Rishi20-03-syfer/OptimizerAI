from django.db import models
from django.contrib.auth.models import User
class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField()
    file = models.FileField(upload_to='files/', null=True,blank=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)

    def __str__(self):
        return self.text

class Expriment(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    audio = models.FileField(upload_to='audios/',null=True,blank=True)
