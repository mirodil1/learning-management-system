from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .manager import UserManager
from onlinedars import settings
from django.urls import reverse

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    # All these field declarations are copied as-is
    # from `AbstractUser`
    STATUS_CHOICES =(
        ('instructor', 'Instructor'),
        ('user', 'User')
    )

    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=12,
        blank=True,
    )
    age = models.IntegerField(
        _('age'),
        null=True,
        blank=True,
    )
    bio = models.TextField(
        _('bio'),
        blank=True,
    )
    picture = models.ImageField(
        _('picture'),
        upload_to=('profile_picture'),
        blank=True,
        default='avatar.png',
    )

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='user')


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug =models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='course_created',
                             on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    cover = models.ImageField(default='default.png',
                                upload_to='images')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images')
    file = models.FileField(upload_to='files')
    video = models.FileField(upload_to='videos')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Permission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.TextField()





















