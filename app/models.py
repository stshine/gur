from django.contrib.auth.models import User
from django.db import models

class Base(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Useflag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=False)
    git_url = models.TextField(null=False)
    upstream_url = models.TextField(null=False)
    license = models.TextField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    maintainer = models.ForeignKey(User, on_delete=models.CASCADE)
    useflags = models.ManyToManyField(Useflag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
