from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True)
    image = models.ImageField(null=True, blank=True, upload_to='categories')

    def __str__(self):
        return self.title


class Drug(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = RichTextUploadingField(blank=True, null=True)
    ingridients = RichTextUploadingField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='drugs')
    # tag = models.ManyToManyField('Tag', blank=True, related_name='drugs')
    image = models.ImageField(null=True, blank=True, upload_to='drugs')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('drug-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Tag(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title
