from django.db import models
from account.models import Account


def get_post_image_filepath(self, filename):
    return 'post_images/' + str(self.pk) + '/post_image.png'


class Post(models.Model):
    text = models.TextField()
    post_image = models.ImageField(null=True, blank=True, upload_to=get_post_image_filepath)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return str(self.author.username) + ' | ' + str(self.text)

    def __str__(self):
        return self.text 

    def get_post_image_filename(self):
        return str(self.post_image)[str(self.post_image).index('post_images/' + str(self.pk) + "/"):]

    class Meta:
        ordering = ['-date_added']



    