from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import datetime

def home(request):
    user = request.user
    skr = datetime.date.today()
    return render(request,'gate/base.html',{'skr': skr, 'user':user,})

