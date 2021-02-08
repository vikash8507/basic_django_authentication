from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfile


class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email=email)

        if user.exists():
            raise forms.ValidationError('Email already registered!')

        return email


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('portfolio_url', 'profile_pic')
