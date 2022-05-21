from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your forms here.
class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta():
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        if len(username) > 150:
            raise
        valid_symbols = ["@",".","+","-","_" ]
        check_symbols = [x for x in username if x in valid_symbols]
        if check_symbols:
            raise
        