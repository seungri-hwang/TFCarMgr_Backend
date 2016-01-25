# -*- coding: utf-8 -*-
import asyncio
from app.data import dataTables

import sys, os


class MemberInsertClass():
	response = {}

	TABLE_NAME = "ML_MEMBER"


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
			if requestDict['method'] == 'read':
				yield from self.read(requestDict)
			if requestDict['method'] == 'update':
				yield from self.update(requestDict)
			if requestDict['method'] == 'delete':
				yield from self.delete(requestDict)
			if requestDict['method'] == 'search':
				yield from self.search(requestDict)
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
			dataUserMasterClass = dataTables.DataTableClass(self.TABLE_NAME)
			conditions = requestDict.get('conditions')
			userEmail = conditions.get('userEmail').lower()
			userName = conditions.get('userName')
			userPassword = conditions.get('userPassword')
			memberID = conditions.get('mmID')

			# 중복 ID CHECK
			queryCondition = {
				"method": "read",
				"conditions":
					{
						"MM_ID" : memberID,
						"MM_USER_EMAIL" : userEmail
					},
				"query": "SELECT DISTINCT * FROM ML_MEMBER WHERE MM_USER_EMAIL = '%s' " % userEmail
			}

			dataUserMasterClassResult = yield from dataUserMasterClass.execute(queryCondition)
			userList = dataUserMasterClassResult

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
				dataUserMasterResult = yield from dataUserMasterClass.execute(queryCondition)
				print(u'---------가입완료')
				self.response = dataUserMasterResult
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

	# create end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def read(self, requestDict):
		self.response = {}

		dataUserMasterClass = dataTables.DataTableClass(self.TABLE_NAME)
		conditions = requestDict.get('conditions')
		memberID = requestDict.get('userNo')
		userEmail = conditions.get('userEmail').lower()

		query = "SELECT FROM "


		queryCondition = {
			"method": "read",
			"conditions":
				{
					"MM_ID" : memberID,
					"MM_USER_EMAIL" : userEmail,
					"MM_USER_NMAE" : memberID
				},
			"query":query
		}


		dataUserMasterClassResult = yield from dataUserMasterClass.execute(queryCondition)
		userList = dataUserMasterClassResult



		return self.response

	# read end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def update(self, requestDict):
		self.response = {}

		return self.response

	# update end --------------------------------------------------------------------------------------------------------------------

	@asyncio.coroutine
	def delete(self, requestDict):
		self.response = {}

		return self.response

		# delete end --------------------------------------------------------------------------------------------------------------------
