from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        help_text="Только буквы, цифры и @ . + - _",
        error_messages={
            'required': 'Пожалуйста, придумайте логин.',
            'unique': 'Этот логин уже занят, попробуйте другой.',
            'invalid': 'В логине можно использовать только буквы, цифры и символы @ . + - _',
        }
    )

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Пароль должен быть не менее 8 символов и не состоять только из цифр.",
        error_messages={
            'required': 'Пожалуйста, придумайте пароль.',
        }
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Введите тот же пароль для проверки.",
        error_messages={
            'required': 'Пожалуйста, подтвердите пароль.',
            'password_mismatch': "Пароли не совпадают, проверьте раскладку или Caps Lock.",
        }
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        error_messages = {
            'password_mismatch': "Пароли не совпадают, попробуйте снова.",
        }