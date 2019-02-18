import logging

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View

from . import constants
from utils.json_fun import to_json_data
from utils.res_code import Code,error_map
from . import models
# Create your views here.


logger = logging.getLogger('django')

class IndexView(View):
    """

    """
    def get(self,request):
        """

        :param request:
        :return:
        """
        tags = models.Tag.objects.only('id', 'name').filter(is_delete=False)

        return render(request, 'news/index.html', locals())

'''
1、创建类视图
2、校验参数
3、从数据库中查询新闻列表数据
4、序列化数据
5、返回给前端
'''

# 1、创建类视图
class NewsListView(View):
    """
    creat news list view
    route:/news/
    # 1、创建类视图
    """

    def get(self,request):
        # 2、校验参数
        try:
            tag_id =int(request.GET.get('tag_id', 0))
        except Exception as e:
            logger.error('标签错误,\n{}'.format(e))
            tag_id = 0
        try:
            page =int(request.GET.get('page', 1))
        except Exception as e:
            # 若用户访问的页数大于实际页数，则返回最后一页数据
            logger.error("当前页数错误：\n{}".format(e))
            page = 1

        # 3、从数据库中查询新闻列表数据
        news_queryset = models.News.objects.select_related('tag','author'). \
            only('title', 'digest', 'image_url', 'update_time', 'tag__name', 'author__username')
        # title , digest, image_url,update__time,author__name,tag__name

        # if models.Tag.objects.only('id').filter(is_delete=False,id=tag_id).exists():
        #     news = news_queryset.filter(is_delete=False,tag_id=tag_id)
        # else:
        #     news = news_queryset.filter(is_delete=False)

        news = news_queryset.filter(is_delete=False, tag_id=tag_id)or \
            news_queryset.filter(is_delete=False)

        paginator = Paginator(news, constants.PER_PAGE_NEWS_COUNT)
        try:
            news_info = paginator.page(page)
        except EmptyPage:
            # 若用户访问的页数大于实际页数，则返回最后一页数据
            logging.info("用户访问的页数大于总页数。")
            news_info = paginator.page(paginator.num_pages)

        # 序列化输出
        news_info_list = []
        for n in news_info:
            news_info_list.append({
                'title': n.title,
                'digest': n.digest,
                'image_url': n.image_url,
                'tag_name': n.tag.name,
                'author': n.author.username,
                'update_time': n.update_time.strftime('%Y年%m月%d日 %H:%M'),
            })

        # 创建返回前端的数据
        data = {
            'total_pages':paginator.num_pages,
            'news': news_info_list
        }

        return to_json_data(data=data)




'''
1、创建类视图
2、
'''
class NewsBanner(View):
    """
    creat news banners view
    route: /news/banners/
    """
    def get(self, request):
        banners = models.Banner.objects.select_related('news').only('image_url', 'news__id', 'news__title'). \
            filter(is_delete=False)[0:constants.SHOW_BANNER_COUNT]
        
        # 序列化输出
        banners_info_list = []
        for b in banners:
            banners_info_list.append({
                'image_url': b.image_url,
                'news_id': b.news.id,
                'news_title': b.news.title,
            })
            # 创建返回给前端的数据
        data = {
            'banners': banners_info_list
        }

        return to_json_data(data=data)

class SerchView(View):

    def get(self, request):
        """

        :param request:
        :return:
        """
        return render(request, 'news/search.html')