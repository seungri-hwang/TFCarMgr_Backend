# -*- coding: utf-8 -*-

import asyncio
import sys,os
from app.service.members import memberInsert


from app.module import moduleDao, moduleHttp


class ControllerClass:
	response = {}

	def __init__(self):
		self.response = {}

	@asyncio.coroutine
	def execute(self, requestDict, daoConnection=None, httpConnection=None):
		# begin = time.time()

		moduleDao.DaoClass.connection = daoConnection
		moduleHttp.HttpClass.connection = httpConnection

		try:
			serviceName = requestDict.get('service', '')
			apiKey = requestDict.get('apiKey', '')

			isAuthorized = True

			# 멤버 조인
			if serviceName == 'members.memberInsert':
				serviceClass = memberInsert.MemberInsertClass()

				serviceResult = yield from serviceClass.execute(requestDict)
				self.response = serviceResult
			else:
				self.response = {
					'isSucceed': False,
					'error': {
						'message': 'You are not authorized to use this service.'
					}
				}
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

		return self.response
