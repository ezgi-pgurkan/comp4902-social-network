from django.db import models
from account.models import Account

class Post(models.Model):
    text = models.TextField()
    post_image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return str(self.author.username) + ' | ' + str(self.text)

    def __str__(self):
        return self.text 
