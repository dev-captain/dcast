from typing import Iterable, Optional
from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext as _
# Create your models here.
import os
import requests
from django.core.files.base import ContentFile


def upload_avatar(instance, filename):
    user_id = str(instance.maker.id)
    return (user_id + "/avatar/" + filename)


def upload_thumbnail(instance, filename):
    user_id = str(instance.maker.id)
    return (user_id + "/thumbnail/" + filename)


def upload_video(instance, filename):
    user_id = str(instance.maker.id)
    return (user_id + "/video/" + filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    last_name = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    birthday_year = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    birthday_month = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    birthday_day = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    gender = models.IntegerField(default=1)
    wedding = models.IntegerField(default=1)
    job = models.CharField(max_length=50, unique=False, blank=True, null=True)
    hobby = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    child = models.BooleanField(default=False)
    salary = models.CharField(
        max_length=50, unique=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    status = models.IntegerField(blank=False, default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "User"


class Video(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    maker = models.ForeignKey(
        User, on_delete=models.CASCADE)
    videoId = models.CharField(
        max_length=255, unique=False, blank=True, null=True)
    title = models.CharField(
        max_length=255, unique=False, blank=True, null=True)
    duration = models.CharField(
        max_length=255, unique=False, blank=True, null=True)
    create_at = models.DateField(auto_now_add=True)
    thumbnail = models.FileField(
        upload_to=upload_thumbnail, blank=True, null=True)
    video = models.FileField(upload_to=upload_video, blank=True, null=True)

    def save_thumbnail(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.basename(url)
            self.thumbnail.save(file_name, ContentFile(
                response.content), save=False)

    def save_video(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.basename(url)
            self.video.save(file_name, ContentFile(
                response.content), save=False)


class AvatarModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    filename = models.FileField(upload_to=upload_avatar)
    maker = models.ForeignKey(User, on_delete=models.CASCADE)
