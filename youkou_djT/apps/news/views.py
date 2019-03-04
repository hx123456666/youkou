import logging
import json

from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
# from django_redis.serializers import json

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
        hot_news = models.HotNews.objects.select_related('news').only('news__title', 'news__image_url',).filter(is_delete=False).order_by('priority', '-news__clicks')[0:constants.SHOW_HOTNEWS_COUNT]

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
                'id': n.id,
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
            filter(is_delete=False).order_by('priority','-update_time', '-id')[0:constants.SHOW_BANNER_COUNT]

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


class NewsDetailView(View):
    """

    """
    def get(self, request, news_id):

        news = models.News.objects.select_related('tag', 'author').only('title', 'content', 'update_time', 'tag__name', 'author__username').filter(is_delete=False, id=news_id).first()

        if news:
            comments = models.Comments.objects.select_related('author', 'parent').only('content', 'author__username', 'update_time', 'parent__author__username', 'parent__content').filter(is_delete=False, news_id=news_id)
            # 序列化输出
            comments_list = []
            for comm in comments:
                comments_list.append(comm.to_dict_data())
            return render(request,'news/news_detail.html', locals())
        else:
            raise Http404("<新闻{}>不存在".format(news_id))
            # return HttpResponseNotFound('<h1>Page not found</h1>')
            # return render(request, '404.html')



# 加一个装饰器或者继承一个拓展类,以判断用户是否登录情况
# method_decologin_required
# 或者class NewsCommentView(LoginRequiredMinxin, View):
class NewsCommentView(View):
    """
    create new comment view
    route: '/news/<int:news_id>/comments/'

    """
    def post(self, request, news_id):
        if not request.user.is_authenticated:
            return to_json_data(errno=Code.SESSIONERR, errmsg=error_map[Code.SESSIONERR])
        if not models.News.objects.only('id').filter(is_delete=False,id=news_id).exists():
            return to_json_data(errno=Code.PARAMERR, errmsg="新闻不存在！")
        try:
            json_data = request.body
            if not json_data:
                return to_json_data(errno=Code.PARAMERR, errmsg="参数为空，请重新输入")
            dict_data = json.loads(json_data.decode("utf8"))
        except Exception as e:
            logger.info("错误信息: \n{}".format(e))
            return to_json_data(errno=Code.UNKOWNERR, errmsg=error_map[Code.UNKOWNERR])

        content = dict_data.get('content')
        if not content:
            return to_json_data(errno=Code.PARAMERR, errmsg="评论内容为空！")


        parent_id = dict_data.get('parent_id')
        try:
            if parent_id:
                parent_id = int(parent_id)
                if not models.Comments.objects.only('id').filter(is_delete=False,id=parent_id,news_id=news_id).exists():
                    return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])

        except Exception as e:
            logger.info("前端传过来的parent_id异常：\n{}".format(e))
            return to_json_data(errno=Code.PARAMERR, errmsg="未知异常")

        # 保存到数据库
        news_comment = models.Comments()
        news_comment.content = content
        news_comment.news_id = news_id
        news_comment.author = request.user
        news_comment.parent_id = parent_id if parent_id else None
        news_comment.save()

        return to_json_data(data=news_comment.to_dict_data())

    # def post(self, request, news_id):
    #
    #
    #     if not request.user.is_authenticated:
    #         return to_json_data(errno=Code.SESSIONERR, errmsg=error_map[Code.SESSIONERR])
    #     if not models.News.objects.only('id').filter(is_delete=False, id=news_id).exists():
    #         return to_json_data(errno=Code.PARAMERR, errmsg="新闻不存在！")
    #
    #
    #
    #     # 从前端获取参数
    #     json_data = request.body
    #     if not json_data:
    #         return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
    #
    #
    #     # 将json转化为dict
    #     dict_data = json.loads(json_data.decode('utf-8'))
    #
    #     content = dict_data.get('content')
    #     if not content:
    #         return to_json_data(errno=Code.PARAMERR, errmsg="评论内容不能为空！")
    #     parent_id = dict_data.get('parent_id')
    #
    #     try:
    #         if parent_id:
    #             parent_id = int(parent_id)
    #             if not models.Comments.objects.only('id').filter(is_delete=False, id=parent_id, news_id=news_id).exists():
    #                 return to_json_data(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
    #
    #
    #     except Exception as e:
    #         logging.info("前端传过来的parent_id异常：\n{}".format(e))
    #         return to_json_data(errno=Code.PARAMERR, errmsg="未知异常")
    #
    #
    #     # 保存到数据库
    #     news_comment = models.Comments()
    #     news_comment.content = content
    #     news_comment.news_id=news_id
    #     news_comment.author = request.user
    #     news_comment.parent_id = parent_id if parent_id else None
    #     news_comment.save()
    #
    #     return to_json_data(data=news_comment.to_dict_data())

