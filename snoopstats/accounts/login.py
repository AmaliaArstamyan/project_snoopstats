from django import forms

class LoginForm(forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address or Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    remember_password = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )