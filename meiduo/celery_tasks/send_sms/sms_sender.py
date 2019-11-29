"""


"""
import time

from celery_tasks.main import app


@app.task(bind=True, name='sms_sender')
def sms_sender(self, mobile, sms_code, expire_time):
	try:
		time.sleep(5)
		# ccp = CCP()
		# result = ccp.send_template_sms(mobile, [sms_code, expire_time], 1)
		# 假设短信发送成功了，如果需要发短信就把这句话删掉，把上面的两句放出来
		result = 0

		print(sms_code)

	except Exception as e:
		result = -1

	else:
		print("短信发送成功...")

	if result == -1:
		self.retry(countdown=15, max_retries=3, exc=Exception("发送短信失败了..."))
