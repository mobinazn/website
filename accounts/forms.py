from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', max_length=254)

    def confirm_login_allowed(self, user):
        return super().confirm_login_allowed(user)


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit = True):
            user = super(UserCreationForm, self).save(commit = False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user 
        

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    