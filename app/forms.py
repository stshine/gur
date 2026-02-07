from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from app.models import Category, Package

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'description', 'upstream_url', 'license', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'upstream_url': forms.URLInput(attrs={'class': 'form-control'}),
            'license': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for f in self.fields:
    #         self.fields[f].widget.attrs['class'] = 'form-control'


    # def save(self, commit=True):
    #     package = super().save(commit=False)
    #     if commit:
    #         package.save()
    #         self.save_m2m()
    #     return package


    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if Package.objects.filter(name=name).exists():
    #         raise forms.ValidationError("Package with this name already exists.")
    #     return name

