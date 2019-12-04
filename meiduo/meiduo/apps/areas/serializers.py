# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 0002 15:20
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: serializers.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from rest_framework import serializers

from .models import Area


class AreaSerializer(serializers.Serializer):
	"""
	行政区划信息序列化器
	"""

	class Meta:
		model = Area
		fields = ('id', 'name')


class SubAreaSerializer(serializers.Serializer):
	"""
	子行政区划信息序列化器
	"""
	subs = AreaSerializer(many=True, read_only=True)

	class Meta:
		model = Area
		fields = ('id', 'name', 'subs')
