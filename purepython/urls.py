from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from fb.views import (
    index, post_details, login_view, logout_view, profile_view,
    edit_profile_view, like_view, view_users, invite_view, view_friends,
    delete_view, delete_post_view, delete_comment_view, album_view,
    new_album_view, add_photos_view, delete_photo_view, delete_album_view,
)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^view_users/$', view_users, name='view_users'),
    url(r'^view_friends/$', view_friends, name='view_friends'),
    url(r'^view_users/(?P<pk>\d)/invite$', invite_view, name='invite_view'),
    url(r'^view_users/(?P<pk>\d)/delete$', delete_view, name='delete_view'),
    url(r'^post/(?P<pk>\d)/$', post_details, name='post_details'),
    url(r'^post/(?P<pk>\d)/delete_post$', delete_post_view, name='delete_post'),
    url(r'^post/(?P<pk>\d)/delete_comment/$', delete_comment_view, name='delete_comment'),
    url(r'^post/(?P<pk>\d)/like$', like_view, name='like'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^profile/(?P<user>\w+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<user>\w+)/edit$', edit_profile_view,
        name='edit_profile'),
    url(r'^profile/(?P<user>\w+)/albums$', album_view,
        name='albums'),
    url(r'^profile/(?P<user>\w+)/albums/add$', new_album_view,
        name='add_album'),
    url(r'^profile/(?P<user>\w+)/albums/(?P<pk>\d)/$', add_photos_view,
        name='photos'),
    url(r'^profile/(?P<user>\w+)/photos/(?P<pk>\d)/delete$', delete_photo_view,
        name='delete'),
    url(r'^profile/(?P<user>\w+)/albums/(?P<pk>\d)/delete$', delete_album_view,
        name='delete_album'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
