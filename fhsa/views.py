from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from fhsa.forms import UserForm, UserProfileForm

# Create your views here.
def index(request):
    context_dict = {'message': "Hello World"}
    return render(request, 'fhsa/index.html', context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'fhsa/register.html',
                  {'user_form': user_form, 'profile_form': profile_form})