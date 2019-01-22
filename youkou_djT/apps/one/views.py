from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from apps.users.models import Users
def index(request):
    return HttpResponse("第一次")


def Delete(request,username):
    Users.objects.filter(name=username).delete()
    return HttpResponse("删除username={}成功".format(username))
