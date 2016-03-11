from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from fhsa.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from identiji import generateAvatar
from .models import UserFolder, UserProfile, User
from searchWrap import bingSearch
import os

@login_required
def home(request):
  return HttpResponse('/fhsa/')

def user_page(request):
    folder = UserFolder.objects.all()
    user = UserProfile.objects.get(user=request.user)
    userorg = User.objects.get(username = request.user)
    avatarSrc = "/fhsastatic/profile_images/" + str(user) + ".png"
    print avatarSrc
    return render(request, 'fhsa/user_page.html', {'user': user, 'folder': folder, 'userorg': userorg, 'avatarSrc': avatarSrc})

def index(request):
    if request.user.is_anonymous():
        return render(request, 'fhsa/index.html', {})
    user = UserProfile.objects.get(user=request.user)
    avatarSrc = "/fhsastatic/profile_images/" + str(user) + ".png"
    return render(request, 'fhsa/index.html', {"avatarSrc":avatarSrc})

def search(request):
    # This will be our view for searching and showing results   
    q = request.GET["query"]
    if q != "":
        result_list = [ [q["DisplayUrl"], q["Description"]] for q in bingSearch(q)]
    return render(request, 'fhsa/search.html', {'result_list': result_list})

def folder(request, folder_name_slug):
    context_dict = {}
    try:
        folder = UserFolder.objects.get(slug=folder_name_slug)
        context_dict['folder_name'] = folder.name

    except UserFolder.DoesNotExist:
        pass

    return render(request, 'fhsa/folder.html', context_dict)

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

            if not os.path.exists("fhsastatic/profile_images"):
                os.mkdir("fhsastatic/profile_images")

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            else:
                profile.avatar = generateAvatar(str(profile.user), "fhsastatic/profile_images")

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
