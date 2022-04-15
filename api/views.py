import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework import exceptions
from rest_framework.versioning import URLPathVersioning
from rest_framework.parsers import JSONParser, FormParser
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response

from api import models
from api.utils import encrypt
from api.utils.permission import SVPPermission
from api.utils.throttle import VisitorThrottle
from api.utils.serializers.pager import PageSerializers


# Create your views here.


class AutoView(APIView):
    """
    用于用户登录认证
    """
    authentication_classes = []  # 认证许可  登录界面不需要认证。[]为不需要验证

    throttle_classes = [VisitorThrottle, ]  # 实现 访问频率控制

    def post(self, request, *args, **kwargs):
        """
        用户登录
        :param request:
        :param args:
        :param kwargs:
        :return: 返回token和基本信息
        """
        ret = {
            'code': 1000,
            'msg': None
        }
        try:
            user = request._request.POST.get("username")
            pwd = request._request.POST.get("password")
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"

            # 进行MD5加密, 为用户登录创建token
            token = encrypt.md5_token(user)
            # 存在就更新， 不存在就创建
            models.UserToken.objects.update_or_create(defaults={"token": token}, user=obj)
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'

        return JsonResponse(ret)


order_dict = [
    {
        "name": "AKL",
        "age": 18,
        "profession": "assassin",
    }, {
        "name": "拉克丝",
        "age": 19,
        "profession": "mage",
    }
]


class OrderView(APIView):
    permission_classes = [SVPPermission, ]  # 访问许可

    # throttle_classes = [UserThrottle, ]  # 访问频率限制

    def get(self, request, *args, **kwargs):

        # 若要实现验证登录， 可通过获取用户token来实现
        # 但这样写比较麻烦, 通过访问许可 SVPPermission来实现
        # token = request._request.GET.get("token")
        # if not token:
        #     return HttpResponse("用户未登录")

        print(request.user)
        print(request.auth)
        ret = {
            'code': 1000,
            'msg': None,
            'data': None
        }
        try:
            ret['data'] = order_dict
        except Exception as e:
            pass
        return JsonResponse(ret)


# 版本控制
class UserView(APIView):
    # versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        print(request.version)
        # 通过reverse反向生成url
        https = request.versioning_scheme.reverse(viewname="user", request=request)
        print(https)
        return HttpResponse('找到version')


# 解析器
class ParserView(APIView):
    # parser_classes = [JSONParser,FormParser,]
    """
        JSONParser:表示只能解析content-type:application/json头
        FormParser:表示只能解析content-type:application/x-www-form-urlencoded头
    """

    def post(self, request, *args, **kwargs):
        """
        允许用户发送JSON格式数据
        a. content-type: application/json
        b. {'name':'alex',age:18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1. 获取用户请求
        2. 获取用户请求体
        3. 根据用户请求头 和 parser_classes = [JSONParser,FormParser,] 中支持的请求头进行比较
        4. JSONParser对象去请求体
        5. request.data
        """

        print(request.data)

        return HttpResponse('ParserView')


# 序列化
"""方法一 继承Serializer
class UserInfoSerializer(serializers.Serializer):
    
    user_type = serializers.CharField(source="get_user_type_display")
    username = serializers.CharField()
    password = serializers.CharField()
    gp = serializers.CharField(source="group")

    rls = serializers.SerializerMethodField()

    def get_rls(self, row):
        role_obj_list = row.roles.all()

        ret = []
        for item in role_obj_list:

            ret.append({"id": item.id, "roles": item.role})

        return ret

"""


class UserInfoSerializer(serializers.ModelSerializer):
    # group = serializers.CharField()
    # 生成链接
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')

    class Meta:
        model = models.UserInfo
        fields = '__all__'
        depth = 1  # 表示连表操作中的取值深度
        """
    def get_group(self, row):
        role_obj_list = row.roles.all()

        ret = []
        for item in role_obj_list:
            ret.append({"id": item.id, "roles": item.role})

        return ret
"""


class UserInfoView(APIView):

    def get(self, request, *args, **kwargs):
        user_info = models.UserInfo.objects.all()
        print("**************")
        # print(type(user_info)) <class 'django.db.models.query.QuerySet'>
        # print(user_info) <QuerySet [<UserInfo:
        # UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>, <UserInfo: UserInfo
        # object (4)>]>
        """
        1. 实例化 一般将数据封装到对象： __new__, __init__
           若many == True,实例化ListSerializer对象   (serializers 164)
           若many == False 实例化 UserInfoSerializer对象
        """
        ser_user_info = UserInfoSerializer(instance=user_info, many=True, context={'request': request})

        """
        2. 调用对象的data属性
        """
        ret = json.dumps(ser_user_info.data, ensure_ascii=False)
        return HttpResponse(ret)


class UserGroupSerializer(serializers.ModelSerializer):
    # group = serializers.SerializerMethodField()
    class Meta:
        model = models.UserGroup
        fields = ['tittle']


class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        groups = models.UserGroup.objects.filter(pk=pk).first()
        # print(type(groups))
        # print(groups)   # groups1
        ser_user_group = UserGroupSerializer(instance=groups, many=False)

        ret = json.dumps(ser_user_group.data, ensure_ascii=False)
        return HttpResponse(ret)


# 分页

class MyPagination(PageNumberPagination):
    # 默认一页显示一个
    page_size = 1

    page_query_param = 'page'
    # 在url中加入&size=2 修改一页显示多少个
    page_size_query_param = "size"

    max_page_size = 20


class PageView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        user = models.UserInfo.objects.all()

        # 创建分页对象
        pg = MyPagination()

        # 在数据库中获取分页数据
        page_roles = pg.paginate_queryset(queryset=user, request=request, view=self)

        # 对数据进行序列化
        ser = PageSerializers(instance=page_roles, many=True)

        # return pg.get_paginated_response(ser.data) 能够实现上下页

        return Response(ser.data)


# 视图

class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = 'size'
    # page_size_query_description = _('Number of results to return per page.')

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 5


class V1View(GenericAPIView):
    # 数据
    queryset = models.UserInfo.objects.all()

    # 序列化
    serializer_class = PageSerializers

    # 分页
    pagination_class = MyCursorPagination

    def get(self, request, *args, **kwargs):
        roles = self.get_queryset()

        page_roles = self.paginate_queryset(roles)

        ser = self.get_serializer(instance=page_roles, many=True)

        return Response(ser.data)
