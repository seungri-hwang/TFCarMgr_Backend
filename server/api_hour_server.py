# -*- coding: utf-8 -*-
# api_hour_server.py
#

import sys
import logging
import asyncio
import ujson
import dicttoxml
import xmltodict
import traceback
import api_hour
import aiohttp.web

from aiohttp.web import Response
from aiohttp.multidict import MultiDict
from app import controller
from app.module import moduleLog, moduleRedis, moduleDao, moduleHttp

sys.path.append('../')

logging.basicConfig(level=logging.INFO)  # enable logging for api_hour

class Container(api_hour.Container):

	daoClass = None
	redisClass = None
	httpClass = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Declare HTTP server
		# print('-----init----- %s'% str(kwargs))
		# self.loop = kwargs['loop']

		self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
		self.servers['http'].ah_container = self  # keep a reference in HTTP server to Container

		# Define HTTP routes
		self.servers['http'].router.add_route('*', '/', self.index)
		self.servers['http'].router.add_route('*', '/healthCheck', self.index)

		# member
		self.servers['http'].router.add_route('*', '/members/memberInsert', self.index)
		self.servers['http'].router.add_route('*', '/members/memberCheckEmail', self.index)
		self.servers['http'].router.add_route('*', '/members/memberList', self.index)
		self.servers['http'].router.add_route('*', '/members/memberEfficiencyInsert', self.index)
		self.servers['http'].router.add_route('*', '/members/memberGet', self.index)

	# A HTTP handler example
	# More documentation: http://aiohttp.readthedocs.org/en/latest/web.html#handler
	@asyncio.coroutine
	def index(self, request):
		if request.path == '/healthCheck' or request.method == 'OPTIONS':
			return Response(text='200',
			                headers=MultiDict(
				                {
					                # 'Content-Type': accept,
					                'Access-Control-Allow-Origin': '*',
					                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Cookie, Accept,X-PINGOTHER',
					                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIOS',
					                'Access-Control-Max-Age': '3600',
					                'Access-Control-Allow-Credentials': 'true'
				                },
			                )
			                )

		result = '{}'
		contentType = request.headers.get('CONTENT-TYPE', 'application/json')

		# pre-flight 요청을 회피하기 위해 json을 text로 받아서 처리한다.
		if contentType == 'text/plain':
			contentType = 'application/json'

		accept = request.headers.get('ACCEPT', 'application/json')
		encoding = request.headers.get('ACCEPT-ENCODING')
		referer = request.headers.get('Referer', '')

		# contentType이 xml이 아니면 json으로 처리
		if contentType != 'application/xml':
			contentType = 'application/json'
		# accept가 xml이 아니면 json으로 처리
		if accept != 'application/xml':
			accept = 'application/json'

		# contentType = 'application/xml'
		# accept = 'application/xml'

		requestDict = {}
		controllerResult = {}

		try:
			body = yield from request.text()
			if body:
				if contentType == 'application/xml':
					body = xmltodict.parse(body)  # convert to OrderedDict
					body = ujson.dumps(body)  # convert to json

				requestDict = {}

				try:
					requestDict = ujson.loads(body)  # json to dict
				except:
					post = yield from request.post()
					requestDict = dict(post)

				# print("post:", post)
				# if len(post) > 0:
				# 	requestDict = dict(post)
				# else:
				# 	requestDict = ujson.loads(body)         # json to dict
				# print("requestDict:", requestDict)

				if contentType == 'application/xml':
					for key, value in requestDict.items():
						requestDict = value
						break

			requestDict['service'] = request.path[1:].replace('/', '.')

			if not requestDict.get('method'):
				# http에서 POST, PUT, DELETE 구분하여 requestDict에 추가
				if request.method == 'POST':
					requestDict['method'] = 'create'
				elif request.method == 'PUT':
					requestDict['method'] = 'update'
				elif request.method == 'DELETE':
					requestDict['method'] = 'delete'
				elif request.method == 'GET':
					requestDict['method'] = 'read'

			controllerClass = controller.ControllerClass()
			controllerResult = yield from controllerClass.execute(requestDict, self.daoClass.connection, self.redisClass.connection, self.httpClass.connection)

			if accept == 'application/xml':
				result = dicttoxml.dicttoxml(controllerResult).decode('utf-8')  # dic to xml
			else:
				if controllerResult.get('service') == 'tools.exportToExcel':
					result = controllerResult
				else:
					result = ujson.dumps(controllerResult)  # dict to json
		except:
			print(traceback.format_exc())

			if accept == 'application/xml':
				result = '<root />'

		def runLogging():
			try:
				logClass = moduleLog.LogClass()
				yield from logClass.execute({}, requestDict, controllerResult)
			except:
				pass

			# asyncio.async(runLogging())

			# print('time server: ', time.time() - begin)

		if controllerResult.get('service') == 'tools.exportToExcel':
			fileName = result.get('condition').get('fileName')
			response = Response(body=result.get('result'),
								headers=MultiDict(
									{
                                        'Pragma' : 'public',
                                        'Expires': '0',
                                        'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
            							'Cache-Control': 'private',  # required for certain browsers,
										'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;',
										'Content-Disposition': 'attachment; filename=%s' % fileName,
										'Content-Transfer-Encoding': 'binary',
										'Access-Control-Allow-Origin': '*',
										'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Cookie, Accept,X-PINGOTHER',
										'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
									},
								)
								)
		elif controllerResult.get('service') == 'tools.virtualBankNotificationReceive':
			result = None
			isSucceed = controllerResult.get('result').get('isSucceed')

			if isSucceed == True:
				result = "OK"
			else:
				result = "FAIL"
			response = Response(text=result,
								headers=MultiDict(
									{
										'Content-Type': 'text/plain',
										'Access-Control-Allow-Origin': '*',
										'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Cookie, Accept,X-PINGOTHER',
										'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
										'Access-Control-Max-Age': '3600',
										'Access-Control-Allow-Credentials': 'true'
									},
								)
							)

		else:
			response = Response(text=result,
								headers=MultiDict(
									{
										'Content-Type': accept,
										'Access-Control-Allow-Origin': '*',
										'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Cookie, Accept,X-PINGOTHER',
										'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
										'Access-Control-Max-Age': '3600',
										'Access-Control-Allow-Credentials': 'true'
									},
								)
								)

		response._keep_alive = True

		# try:
		# 	if 'travelhow.com' in referer:
		# 		if 'gzip' in encoding or 'deflate' in encoding:
		# 			response.enable_compression(True)
		# except:
		# 	pass

		return response

	# Container methods
	@asyncio.coroutine
	def start(self):
		yield from super().start()
		print('server started.')

		try:
			self.daoClass = moduleDao.DaoClass()
			asyncio.async(self.daoClass.open())

			self.redisClass = moduleRedis.RedisClass()
			asyncio.async(self.redisClass.open())

			self.httpClass = moduleHttp.HttpClass()
			asyncio.async(self.httpClass.open())
		except:
			print(traceback.format_exc())

	# self.engines['pg'] = self.loop.create_task(aiopg.create_pool(host=self.config['engines']['pg']['host'],
	#                                                              port=int(self.config['engines']['pg']['port']),
	#                                                              sslmode='disable',
	#                                                              dbname=self.config['engines']['pg']['dbname'],
	#                                                              user=self.config['engines']['pg']['user'],
	#                                                              password=self.config['engines']['pg']['password'],
	#                                                              cursor_factory=psycopg2.extras.RealDictCursor,
	#                                                              minsize=int(self.config['engines']['pg']['minsize']),
	#                                                              maxsize=int(self.config['engines']['pg']['maxsize']),
	#                                                              loop=self.loop))
	# yield from asyncio.wait([self.engines['pg']], return_when=asyncio.ALL_COMPLETED)


	@asyncio.coroutine
	def stop(self):
		# A coroutine called when the Container is stopped
		# LOG.info('Stopping engines...')

		# if 'pg' in self.engines:
		#     if self.engines['pg'].done():
		#         self.engines['pg'].result().terminate()
		#         yield from self.engines['pg'].result().wait_closed()
		#     else:
		#         yield from self.engines['pg'].cancel()
		#     LOG.info('All engines stopped !')
		try:
			if self.daoClass is not None:
				asyncio.async(self.daoClass.close())

			if self.redisClass is not None:
				asyncio.async(self.redisClass.close())

			if self.httpClass is not None:
				asyncio.async(self.httpClass.close())
		except:
			print(traceback.format_exc())

		yield from super().stop()

	def make_servers(self):
		# This method is used by api_hour command line to bind your HTTP server on socket
		return [self.servers['http'].make_handler(logger=self.worker.log,
		                                          keep_alive=self.worker.cfg.keepalive,
		                                          access_log=self.worker.log.access_log,
		                                          access_log_format=self.worker.cfg.access_log_format)]

	# handlers = {}
	# handler = self.servers['http'].make_handler(logger=self.worker.log,
	#                                             keep_alive=self.worker.cfg.keepalive,
	#                                             access_log=self.worker.log.access_log,
	#                                             access_log_format=self.worker.cfg.access_log_format)
	# # for sock in sockets:
	# #     srv = yield from self.loop.create_server(handler, sock=sock.sock)
	# #     handlers[srv] = handler
	#
	# return handlers