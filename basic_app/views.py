from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'basic_app/index.html')


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

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render(request, 'basic_app/register.html', context)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('<h2>User with enter credentials no longer active!</h2>')
        else:
            return HttpResponse('<h2>Please enter correct username and password!</h2>')

        print(username, password)
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'basic_app/login.html')


@login_required
def profile(request):
    return HttpResponse('You are loged in!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponse('You are successfully logged out!')
