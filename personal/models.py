from django.db import models
from account.models import Account


def get_post_image_filepath(self, filename):
    return 'post_images/' + str(self.pk) + '/post_image.png'


class Post(models.Model):
    text = models.TextField()
    post_image = models.ImageField(null=True, blank=True, upload_to=get_post_image_filepath)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(Account, related_name="postlikes", blank=True)

    def str(self):
        return str(self.author.username) + ' | ' + str(self.text)

    def __str__(self):
        return self.text 

    def get_post_image_filename(self):
        return str(self.post_image)[str(self.post_image).index('post_images/' + str(self.pk) + "/"):]

    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        ordering = ['-date_added']


LIKE_CHOICES = (
('Like', 'Like'),
('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)


    def __str__(self):
        return f"{self.user}-{self.post}- {self.value}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def str(self):
        return str(self.author.username) + ' | ' + str(self.body)

    def __str__(self):
        return self.body 
