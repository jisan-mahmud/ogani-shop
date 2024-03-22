from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


    def save(self, commit=False):
        user = super().save(commit=False)
        if commit:
            try:
                username = self.cleaned_data.get('email').split('@')[0]
                user.username = username
                user.is_active = False
                user.save()
            except:
                pass
        return user



    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2



    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(login_form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})