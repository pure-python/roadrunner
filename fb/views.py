from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

from fb.models import UserPost, UserPostComment, UserProfile, Album, Photo
from fb.forms import (
    UserPostForm, UserPostCommentForm, UserLogin, UserProfileForm, AlbumForm, PhotoForm
)


@login_required
def index(request):
    posts = UserPost.objects.all()
    if request.method == 'GET':
        form = UserPostForm()
    elif request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            post = UserPost(text=text, author=request.user)
            post.save()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


@login_required
def post_details(request, pk):
    post = UserPost.objects.get(pk=pk)

    if request.method == 'GET':
        form = UserPostCommentForm()
    elif request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = UserPostComment(text=cleaned_data['text'],
                                      post=post,
                                      author=request.user)
            comment.save()

    comments = UserPostComment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_details.html', context)


def login_view(request):
    if request.method == 'GET':
        login_form = UserLogin()
        context = {
            'form': login_form,
        }
        return render(request, 'login.html', context)
    if request.method == 'POST':
        login_form = UserLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': login_form,
                'message': 'Wrong user and/or password!',
            }
            return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    if not request.user == profile.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
        }
        avatar = SimpleUploadedFile(
            profile.avatar.name, profile.avatar.file.read()) \
            if profile.avatar else None
        file_data = {'avatar': avatar}
        form = UserProfileForm(data, file_data)
    elif request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.save()

            profile.gender = form.cleaned_data['gender']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']
            profile.save()

            return redirect(reverse('profile', args=[profile.user.username]))
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def like_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.likers.add(request.user)
    post.save()
    return redirect(reverse('post_details', args=[post.pk]))


@login_required
def view_users(request):
    users = User.objects.all()
    if request.method == 'GET':
        context = {
            'users': users,
        }

    return render(request, 'view_users.html', context)

@login_required
def invite_view(request,pk):
    if request.method == 'GET':
        user1 = request.user
        user2 = User.objects.get(pk=pk)
        user1.profile.friends.add(user2)
        user2.profile.friends.add(user1)
        user1.profile.save()
        user2.profile.save()
    users = User.objects.all()
    context = {
            'users': users,
        }
    return render(request, 'view_users.html', context)

@login_required
def delete_view(request,pk):
    if request.method == 'GET':
        user1 = request.user
        user2 = User.objects.get(pk=pk)
        user1.profile.friends.remove(user2)
        user2.profile.friends.remove(user1)
        user1.profile.save()
        user2.profile.save()
    users = User.objects.all()
    context = {
            'users': users,
        }
    return render(request, 'view_users.html', context)

@login_required
def view_friends(request):
    friends = request.user.profile.friends.all()
    if request.method == 'GET':
        context = {
            'friends': friends,
        }

    return render(request, 'view_friends.html', context)


@login_required
def delete_post_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.delete()
    return redirect(reverse('index'))


def delete_comment_view(request, pk):
    comment = UserPostComment.objects.get(pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect(reverse('post_details',args=[post_pk]))


def album_view(request, user):
    albums = Album.objects.filter(user__username=user)
    profile = UserProfile.objects.get(user__username=user)
    context = {
        'profile': profile,
        'albums': albums,
    }
    return render(request, 'albums.html', context)


def new_album_view(request, user):
    if request.method == 'GET':
        form = AlbumForm()
    elif request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            album = Album()
            if cleaned_data['album_name']:
                album.album_name = cleaned_data['album_name']
            if cleaned_data['album_date']:
                album.album_date = cleaned_data['album_date']
            album.user = User.objects.get(username=user)
            album.save()
            return redirect(reverse('albums', args=[user]))
    context = {
        'form': form,
    }
    return render(request, 'add_album.html', context)


def photos_view(request, user, pk):
    photos = Photo.objects.filter(album__id=pk)
    context = {
        'photos': photos,

    }
    return render(request, 'photos.html', context)


def add_photos_view(request, user, pk):
    album = Album.objects.get(pk=pk)
    if request.method == 'GET':
        form = PhotoForm()
    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['photo']:
                photo = Photo(photo=form.cleaned_data['photo'])
                album.photos.add(photo)
                photo.save()
                album.save()
            return redirect(reverse('photos', args=[user, pk]))
    context = {
        'form': form,
        'photos': album.photos,
    }
    return render(request, 'photos.html', context)


def delete_photo_view(request,user,  pk):
    photo = Photo.objects.get(pk=pk)
    album = photo.album
    photo.delete()
    return redirect(reverse('photos', args=[user, album.pk]))


def delete_album_view(request, user, pk):
    album = Album.objects.get(pk=pk)
    album.delete()
    return redirect(reverse('albums', args=[user]))
