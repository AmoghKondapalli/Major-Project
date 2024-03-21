from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()