from django.shortcuts import render
from django.views import View

from . import models
# Create your views here.



class IndexView(View):
    """

    """
    def get(self,request):
        """

        :param request:
        :return:
        """
        tags = models.Tag.objects.only('id','name').filter(is_delete=False)

        return render(request,'news/index.html',locals())






def serch(request):
    return render(request,'news/search.html')
