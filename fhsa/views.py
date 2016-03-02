from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from fhsa.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from identiji import generateAvatar
from .models import UserFolder, UserProfile, User
import os

@login_required
def home(request):
  return HttpResponse('/fhsa/')

def user_page(request):
    folder = UserFolder.objects.all()
    user = UserProfile.objects.get(user=request.user)
    userorg = User.objects.get(username = request.user)
    return render(request, 'fhsa/user_page.html', {'user': user, 'folder': folder, 'userorg': userorg})

def index(request):
    return render(request, 'fhsa/index.html', {})

def folder(request, folder_id):
    folder = get_object_or_404(UserFolder, pk=id)
    return render(request, 'fhsa/folder.html', {'folder': folder})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/fhsa/')

def about(request):
    return render(request, 'fhsa/about.html', {})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if not os.path.exists("profile_images"):
                os.mkdir("profile_images")

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            else:
                profile.avatar = generateAvatar(str(profile.user), "static/profile_images")

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'fhsa/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
