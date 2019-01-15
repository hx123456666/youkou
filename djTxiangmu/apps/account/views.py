from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse
from django.views import View
from .forms import LoginForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator


# 不验证 CSRF csrf_exempt

# 验证 CSRF csrf_protect  context 用在 render 模板渲染
@method_decorator([csrf_exempt, ], name='dispatch')
class LoginView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'account/login.html')

    def post(self, request, *args, **kwargs):
        # telephone = request.POST.get("telephone")
        form = LoginForm(request.POST)
        # 如果验证通过 继续
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone", None)
            password = form.cleaned_data.get('password', None)
            # print(telephone, password)

            # alt + enter
            user = authenticate(username=telephone,
                               password=password)
            if user:
                login(request, user)
                # return redirect(reverse(''))
                return JsonResponse({"code": 2, "msg": "登录成功", "data": "xxx"})
            return JsonResponse({"code": 1, "msg": "用户名或密码错误"})
        # <ul class="errorlist"><li>telephone<ul class="errorlist"><li>长度有误</li></ul></li></ul>

        # API 文档 是后端写的  直接自己写

        #  json
        # error_json =  form.errors.get_json_data()

        # print(form.errors)


        # return HttpResponse(json.dumps({"code": 1, "msg": "xsxx错误"}))

        # return  HttpResponse("xx")
        return JsonResponse({"code": 1, "msg": form.get_error()})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'account/register.html')
    def post(self, request, *args, **kwargs):
        pass

# def login(request):

#     if request.method == 'POST':

#         return 'xx'

#     return render(request, 'account/login.html')


"""
### 一般来说 如果说你的只有一个get

   def xx(request):
      if request.method == 'GET':


        xxx


   elif request.method == 'POST'
"""