from django.shortcuts import render

# Create your views here.

def index(request):
    """
    index page
    :param request:
    :return:
    """
    return render(request,'news/index.html')

def serch(request):
    return render(request,'news/search.html')