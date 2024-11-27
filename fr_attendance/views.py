from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from .models import Todo
# from .forms import TodoForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# from django.http import HttpResponse


# def home_page(request):
#     return HttpResponse("Welcome to the home page!")
@login_required
def home_page(request):
    return render(request, "fr_attendance/user_home.html")
