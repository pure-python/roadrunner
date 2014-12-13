from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.utils import OperationalError
from django.dispatch import receiver
from django.templatetags.static import static
from django.conf import settings


class UserPost(models.Model):
    text = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, related_name='posts')
    likers = models.ManyToManyField(User, related_name='liked_posts')

    def __unicode__(self):
        return '{} @ {}'.format(self.author, self.date_added)

    class Meta:
        ordering = ['-date_added']


class UserPostComment(models.Model):
    text = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User)
    post = models.ForeignKey(UserPost)

    def __unicode__(self):
        return '{} @ {}'.format(self.author, self.date_added)

    class Meta:
        ordering = ['date_added']


class UserProfile(models.Model):
    GENDERS = (
        ('-', 'Unknown'),
        ('F', 'Female'),
        ('M', 'Male'),
    )
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='-')
    avatar = models.ImageField(upload_to='images/', blank=False, null=True)

    user = models.OneToOneField(User, related_name='profile')

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar \
            else static(settings.AVATAR_DEFAULT)


class Album(models.Model):
    album_name = models.CharField(max_length=200, default="New Album")
    album_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='albums')


class Photo(models.Model):
    photo = models.ImageField(upload_to='images/', blank=False, null=True)
    album = models.ForeignKey(Album, related_name='photos')

@receiver(post_save, sender=User)
def callback(sender, instance, *args, **kwargs):
    if not hasattr(instance, 'profile'):
        instance.profile = UserProfile()
        try:
            instance.profile.save()
        except OperationalError:
            pass
