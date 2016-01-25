# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import time, datetime
from app.module import moduleLog
import traceback

class HttpClass():

	connection = None

	def __init__(self):
		pass

	@asyncio.coroutine
	def open(self):
		if HttpClass.connection is not None:
			if HttpClass.connection.closed:
				HttpClass.connection = None

		if HttpClass.connection is None:
			HttpClass.connection = aiohttp.TCPConnector(limit=1000, verify_ssl=False, keepalive_timeout=60, use_dns_cache=True, force_close=True)
			print('http opened.')

	@asyncio.coroutine
	def close(self):
		if HttpClass.connection is not None:
			if not HttpClass.connection.closed:
				HttpClass.connection.close()
				print('http closed.')

	@asyncio.coroutine
	def execute(self, url=None, method='GET', headers=None, body=None, sender=None, logInfo={}):
		if url == 'null' or url is None:
			return ''

		begin = time.time()
		beginDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

		result = ''

		try:
			yield from self.open()

			if headers == None:
				headers = {'Connection': 'keep-alive'}

			response = yield from asyncio.wait_for(aiohttp.request(method, url=url, headers=headers, connector=HttpClass.connection, data=body), 10)
			# print('-' * 30, url, '-' * 30)
			# response = yield from aiohttp.request(method, url=url, headers=headers, connector=HttpClass.connection,data=body)
			# assert response.status == 200

			# data = yield from response.read_and_close()		#binary로 리턴된다.(gzip)
			data = yield from response.read()  # binary로 리턴된다.(gzip)

			response.close()

			# result = len(data)
			result = data.decode('utf-8')
		except asyncio.TimeoutError:
			pass
		except:
			print(traceback.format_exc())

		end = time.time()
		endDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

		# log

		# 'vendorCompCode' : self.vendorCompCode ,
  #               'bookingItemCode' : '',
  #               'sellerCompCode' : '',
  #               'apiPath' : url,
  #               'serviceName' : self.serviceName,
  #               'actionName' : self.actionName,
  #               'request' : requestXml, # 전문
  #               'response': '',
  #               'beginDateTime' : '',
  #               'endDateTime': '',
  #               'duration': self.timeOut,
  #               'deviceToken' : '',
  #               'os' : '',
  #               'browser' : '',
  # #               'firstInsertTime' : ''
		if logInfo is not None:
			def runLogProcess():
				try:
					logInfo['apiPath'] = url
					logInfo['request'] = str(body)
					logInfo['response'] = str(result)
					logInfo['beginDateTime'] = beginDateTime
					logInfo['endDateTime'] = endDateTime
					logInfo['duration'] = end - begin

					logClass = moduleLog.LogClass()
					yield from logClass.execute(logInfo)
				except:
					print(traceback.format_exc())

			asyncio.async(runLogProcess())

		# try:
		# 	open('moduleHttp.txt', 'a').write('''
		# 		=================================================================================
		# 		%s
		# 		=================================================================================
		# 		 ''' % (str(body)))
		#
		# 	open('moduleHttp.txt', 'a').write('''
		# 			=================================================================================
		# 			%s
		# 			=================================================================================
		# 			 ''' % (str(result)))
		#
		# except:
		# 	print(traceback.format_exc())

		# print('[moduleHttp.execute.%s]: ' % sender, end-begin)

		return result
