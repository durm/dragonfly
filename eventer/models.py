from django.db import models
from django.contrib.auth.models import User

class Proto(models.Model):

    name = models.CharField(max_length=512, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="products", null=True, blank=True)
    thumb = models.ImageField(upload_to="products", null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="+", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_by = models.ForeignKey(User, related_name="+", blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Category(Proto):
    parent = models.ForeignKey('self', null=True, blank=True)

    def getchildren(self):
        return Category.objects.filter(parent=self)

    @staticmethod
    def get_roots():
        return Category.objects.filter(parent=None)

class Product(Proto):
    categories = models.ManyToManyField(Category)

class WList(Proto):
    products = models.ManyToManyField(Product)

class SEvent(Proto):
    place = models.CharField(max_length=512)
    time = models.CharField(max_length=512)
    members = models.ManyToManyField(User)
