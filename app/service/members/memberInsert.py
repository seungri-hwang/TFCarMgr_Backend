# -*- coding: utf-8 -*-
import asyncio
from app.data import dataTables

import sys, os


class MemberInsertClass():
	response = {}

	def __init__(self):

		self.response = {}
		self.keys = []

	# __init__ end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def execute(self, requestDict):
		self.response = requestDict
		try:
			if requestDict['method'] == 'create':
				yield from self.create(requestDict)
		except:
			pass

		return self.response

	@asyncio.coroutine
	def search(self, requestDict):
		pass

	@asyncio.coroutine
	def create(self, requestDict):
		self.response = requestDict

		try:
			dataUserMasterClass = dataTables.DataTableClass('ML_MEMBER')
			conditions = requestDict.get('conditions')
			userEmail = conditions.get('userEmail').lower()
			userName = conditions.get('userName')
			userPassword = conditions.get('userPassword')
			memberID = requestDict.get('userNo')

			# 중복 ID CHECK
			queryCondition = {
				"method": "read",
				"conditions":
					{
						"MM_ID" : memberID,
						"MM_USER_EMAIL" : userEmail
					}
			}

			dataUserMasterClassResult = yield from dataUserMasterClass.execute(queryCondition)
			userList = dataUserMasterClassResult


			print(userList)

			if 0 < len(userList.get('result').get('list')):
				message = u'-------이미 가입한 회원입니다.'
				print(message)
				result = {
					'result': {
						'isSucceed': False,
						'error': {
							'message': message
						}
					}
				}
				self.response = result

			else:
				rows = {"MM_ID" : memberID,"MM_USER_EMAIL" : userEmail,"MM_USER_NAME" : userName,"MM_USER_PASSWORD" : userPassword }
				queryCondition = {
					"method": "create",
					"conditions": {
						"rows": [rows]
					}
				}

				print(u'---------가입완료')
				dataUserMasterResult = yield from dataUserMasterClass.execute(queryCondition)
				self.response = dataUserMasterResult
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

	# create end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def read(self):
		self.response = {}

		return self.response

	# read end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def update(self):
		self.response = {}

		return self.response

	# update end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def delete(self):
		self.response = {}

		return self.response

		# delete end --------------------------------------------------------------------------------------------------------------------
