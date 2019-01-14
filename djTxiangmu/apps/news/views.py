from django.shortcuts import render


def index(request):
    return render(request, 'news/index.html')


def search(request):
    return render(request, 'news/search.html')