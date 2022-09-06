from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField, CharField, HiddenInput

from .models import Ticket, CustomUser


class NewTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'files']


class UpdateTicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateTicketForm, self).__init__(*args, **kwargs)
        self.fields['worker'].queryset = CustomUser.objects.filter(
            role__in=[CustomUser.ADMIN_ROLE, CustomUser.REGULAR_ROLE])
        self.fields['customer'].queryset = CustomUser.objects.filter(role=CustomUser.CUSTOMER_ROLE)

    class Meta:
        model = Ticket
        fields = '__all__'


class LoginForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RespondTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['response']


class SignupForm(UserCreationForm):
    email = EmailField(required=True)
    role = CharField(widget=HiddenInput(), initial=CustomUser.CUSTOMER_ROLE)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewUserForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UpdateUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")
