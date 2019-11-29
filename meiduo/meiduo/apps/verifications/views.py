# Create your views here.
import random

from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from celery_tasks.send_sms.sms_sender import sms_sender
from meiduo.libs.captcha.captcha import captcha
from meiduo.utils.response_code import RET
from . import constants


class ImageCodeView(APIView):
	"""
	re_path('^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
	图片验证码
	"""

	def get(self, request, image_code_id):
		"""
		获取图片验证码
		:param request:
		:param image_code_id:
		:return:
		"""
		# 生成验证码图片
		text, image = captcha.generate_captcha()

		# django-redis提供了get_redis_connection的方法，通过调用get_redis_connection方法传递redis的配置名称
		# 可获取到redis的连接对象，通过redis连接对象可以执行redis命令,在settings配置
		image_code_id = "image_code_" + image_code_id
		redis_conn = get_redis_connection("code")
		redis_conn.setex(name=image_code_id, time=constants.REDIS_IMAGE_CODE_EXPIRE, value=text)

		# 固定返回验证码图片数据，不需要DRF框架的Response帮助我们决定返回相应数据的格式
		# 此处直接使用django原生的httpresponse即可
		return HttpResponse(image, content_type='images/jpg')


class SmsCodeView(GenericAPIView):
	"""
	url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view())
	短信验证码
	"""

	def get(self, request, mobile):
		"""
		创建短信验证码
		:param request:
		:param mobile:
		:return:
		"""
		image_code = request.GET.get("image_code")
		image_code_id = request.GET.get("image_code_id")

		# 判断图片验证码是否为空
		if not all([image_code, image_code_id]):
			return JsonResponse({"code": RET.PARAMERR, "errmsg": "参数不全"})

		# 与缓存图片验证码对比
		redis_conn = get_redis_connection("code")
		redis_image_code = redis_conn.get("image_code_%s" % image_code_id)
		# 删除验证码
		redis_conn.delete("image_code_%s" % image_code_id)

		if not redis_image_code:
			return JsonResponse({"code": RET.NODATA, "errmsg": "验证码过期"})

		if not image_code.lower() == redis_image_code.decode().lower():
			return JsonResponse({"code": RET.DATAERR, "errmsg": "图片验证码输入有误"})

		# 验证前后两次发送短信时间间隔是否大于60s
		if redis_conn.get("send_flag_%s" % mobile):
			return JsonResponse({"code": RET.SMSCODERR, "errmsg": "发送短信太频繁"})

		# 发送短信
		sms_code = "%06d" % random.randint(0, 999999)

		# 用celery去发送短信
		sms_sender.delay(mobile, sms_code, constants.REDIS_SMS_CODE_EXPIRES // 60)

		# 用pipe方法（类似于事务）
		pipeline = redis_conn.pipeline()
		pipeline.setex("sms_code_%s" % mobile, constants.REDIS_SMS_CODE_EXPIRES, sms_code)

		# 把时间间隔写入数据库
		pipeline.setex("send_flag_%s" % mobile, constants.REDIS_SEND_FLAG_EXPIRES, 1)

		pipeline.execute()

		return JsonResponse({"code": RET.OK, "errmsg": "发送成功"})
