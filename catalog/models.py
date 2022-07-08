from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=255, default='')
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    script = models.TextField()
    post_time = models.DateTimeField(auto_now=True)
    thumnail = models.ImageField(null=True, upload_to='products/thumnails/')
    category = models.ManyToManyField(Category, related_name='category')
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title + ' | ' + self.author.first_name + " " + self.author.last_name

    def get_absolute_url(self):
        return reverse('category')


class ProductImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(null=True, upload_to='products/images/')

    def __str__(self):
        return self.post.title


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'

    def children(self):
        return Comments.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True