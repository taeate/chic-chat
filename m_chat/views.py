from django.shortcuts import render


def home(request):
    return render(request, 'm_base/m_layout.html')