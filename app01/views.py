import json

from django.shortcuts import render, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView, Request
from rest_framework import exceptions


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class Student(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("获取学生")

    def post(self, request, *args, **kwargs):
        return HttpResponse("创建学生")

    def put(self, request, *args, **kwargs):
        return HttpResponse("更新学生")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("删除学生")


@csrf_exempt
def user(request):
    if request.method == 'GET':
        return HttpResponse('获取用户')

    elif request.method == 'POST':
        return HttpResponse('创建用户')

    elif request.method == 'PUT':
        return HttpResponse('更新用户')

    elif request.method == 'DELETE':
        return HttpResponse('删除用户')


class MyAuthentication(object):
    def authenticate(self, request):
        token = request._request.GET.get("token")
        if not token:
            raise exceptions.NotAuthenticated("用户认证失败")
        return ("Alex", None)

    def authenticate_header(self, val):
        pass


class MyRequest(Request):

    def user(self):
        print("我是user")


class MyView(View):

    def initialize_request(self, request, *args, **kwargs):
        return MyRequest(request)


class DogView(MyView, APIView):
    # authentication_classes = [MyAuthentication, ]

    # def dispatch(self, request, *args, **kwargs):
    #   return

    def get(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': "xxx"
        }
        return HttpResponse(json.dumps(ret), status=201)

    def post(self, request, *args, **kwargs):
        return HttpResponse("创建dog")

    def put(self, request, *args, **kwargs):
        return HttpResponse("更新dog")

    def delete(self, request, *args, **kwargs):
        return HttpResponse("删除dog")
