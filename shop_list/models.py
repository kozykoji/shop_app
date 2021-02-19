from django.db import models
from django.core.validators import URLValidator
from accounts.models import CustomUser
from django.urls import reverse
from django.utils import timezone
import uuid

# Create your models here.

GENRE_CHOICES = (
    ('メンズ', 'メンズ'),
    ('ウィメンズ', 'ウィメンズ'),
    ('メンズ・ウィメンズ', 'メンズ・ウィメンズ'),
)
TREAT_USED_CHOICES = (
    ('有','有'),
    ('無','無'),
)

class TreatBrands(models.Model):
    brandname = models.CharField('ブランド名', max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.brandname 

class List(models.Model):
    class Meta:
        db_table = 'post'
    shopname = models.CharField('店名',max_length=200)
    treatbrand = models.CharField(max_length=200)
    treat_brand = models.ManyToManyField(TreatBrands, '取扱ブランド')
    treatused = models.CharField('古着の取扱',max_length=200, choices=TREAT_USED_CHOICES)
    genre =  models.CharField('ジャンル',max_length=200, choices=GENRE_CHOICES)
    address = models.CharField('所在地',max_length=200)
    hpurl = models.TextField('ホームページURL',validators=[URLValidator()], blank=True, null=False)

    def __str__(self):
        return self.shopname 

class Review(models.Model):
    post = models.ForeignKey(List, on_delete=models.CASCADE, related_name='review')
    review = models.TextField(max_length=255)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.review 


class Comment(models.Model):
    post = models.ForeignKey(List, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text 