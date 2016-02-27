from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from fhsa.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from identiji import generateAvatar
import os

@login_required
def home(request):
  return HttpResponse('/fhsa/')

def index(request):
    context_dict = {'message': "Hello World"}
    return render(request, 'fhsa/index.html', context_dict)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/fhsa/')

def about(request):
    return render(request, 'fhsa/about.html', {})

def register(request):
    """
    TODO: Currently not working, will need to fix
    """
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Check that the profile images directory exists - this is the one we used in the model
            if not os.path.exists("profile_images"):
                os.mkdir("profile_images")

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            else:
                profile.avatar = generateAvatar(str(profile.user), "profile_images")

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'fhsa/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
