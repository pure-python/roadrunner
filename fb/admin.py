from django.contrib import admin

from fb.models import UserPost, UserProfile, Photo, Album


admin.site.register(UserPost)
admin.site.register(UserProfile)
admin.site.register(Album)
admin.site.register(Photo)
