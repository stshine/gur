from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Category(Base):
    name = models.CharField(max_length=127, unique=True)

    def __str__(self) -> str:
        return self.name


class Useflag(Base):
    name = models.CharField(max_length=127, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Package(Base):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    git_url = models.CharField(max_length=511)
    upstream_url = models.CharField(max_length=511)
    license = models.CharField(max_length=127)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    maintainer = models.ForeignKey(User, on_delete=models.CASCADE)
