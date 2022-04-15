"""djangoandrest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', views.AutoView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('user/', views.UserView.as_view(), name="user"),
    path('parser/', views.ParserView.as_view(), name="user"),
    path('userInfo/', views.UserInfoView.as_view(), name="userInfo",),
    path('userInfo/group/<int:pk>/', views.GroupView.as_view(), name="gp",),
    path('userInfo/page/', views.PageView.as_view()),
    path('userInfo/v1/', views.V1View.as_view()),

    ]
