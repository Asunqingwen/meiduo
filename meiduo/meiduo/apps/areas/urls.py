# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 0003 15:00
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: urls.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
]

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='areas')

urlpatterns += router.urls
