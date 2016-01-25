
# -*- coding: utf-8 -*-

import asyncio
import sys, io
from pymongo import MongoClient

class LogClass():
	def __init__(self):
		pass

	@asyncio.coroutine
	def execute(self, logInfo={}, request={}, response={}):
		try:
			logType = logInfo.get('logType')

			if logInfo.get('logType'):
				logInfo.pop('logType', None)
			if logType == 'search':
				logInfo.pop('bookingItemCode', None)

			# requstDict = {
			# 	'method': 'create',
			# 	'condition': {
			# 		'rows': [logInfo]
			# 	}
			# }


			# dataVendorBookingTransactionLogClass = dataTables.DataVendorBookingTransactionLogClass()
			# dataVendorBookingTransactionLogResult = yield from dataVendorBookingTransactionLogClass.execute(requstDict)
			# elif logType == 'search':
			# 	dataVendorSearchTransactionLogClass = dataTables.DataVendorSearchTransactionLogClass()
			# 	dataVendorSearchTransactionLogResult = yield from dataVendorSearchTransactionLogClass.execute(requstDict)

			collectionName = 'apiTransactionLog'
			if logType == 'booking':
				collectionName = 'bookingTransactionLog'
			elif logType == 'search':
				collectionName = 'searchTransactionLog'

			client = MongoClient('52.192.99.156', 27017)
			logDB = client['TravelHowLog']

			collection = logDB[collectionName]
			logData = {
				'request': request,
				'response': response
			}
			collection.insert_one(logData)
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)
