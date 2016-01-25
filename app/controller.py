# -*- coding: utf-8 -*-

import asyncio
import sys,os
from app.service.members import memberInsert,memberGet


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

			# 멤버 조인
			if serviceName == 'members.memberInsert':
				serviceClass = memberInsert.MemberInsertClass()

			# 멤버 조희
			elif serviceName == 'members.memberGet':
				serviceClass = memberGet.MemberGetClass()

			serviceResult = yield from serviceClass.execute(requestDict)
			self.response = serviceResult

		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

		return self.response
