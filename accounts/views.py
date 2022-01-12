from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.shortcuts import render, redirect


def accounts(request):
    return render(request, 'accounts_login.html')


def login(request: HttpRequest):
    return render(request, 'login.html')
