# -*- coding: utf-8 -*-
# api_hour_server.py
#

import sys, os

sys.path.append('../')

from app import controller
from app.module import moduleDao, moduleHttp

import logging
import asyncio

import api_hour
import aiohttp.web
from aiohttp.web import Response
from aiohttp.multidict import MultiDict

import ujson
import dicttoxml, xmltodict
import traceback

logging.basicConfig(level=logging.INFO)  # enable logging for api_hour


class Container(api_hour.Container):

   daoClass = None
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

      # Members
      self.servers['http'].router.add_route('*', '/members/memberInsert', self.index)
      self.servers['http'].router.add_route('*', '/members/memberGet', self.index)
      self.servers['http'].router.add_route('*', '/members/memberList', self.index)

      # 차량조회
      self.servers['http'].router.add_route('*', '/vehicles/vehicleInsert', self.index)
      self.servers['http'].router.add_route('*', '/vehicles/vehicleCheckNumber', self.index)
      self.servers['http'].router.add_route('*', '/vehicles/vehicleDelete', self.index)

      # 운행조회
      self.servers['http'].router.add_route('*', '/statusTypes/statusTypeList', self.index)

      # 구분조회
      self.servers['http'].router.add_route('*', '/statusSorts/statusSortsList', self.index)

      # 회원 연비계산
      self.servers['http'].router.add_route('*', '/memberEfficiencies/memberEfficiencyInsert', self.index)
      self.servers['http'].router.add_route('*', '/memberEfficiencies/memberEfficiencyGet', self.index)

      # 연비계산방식
      self.servers['http'].router.add_route('*', '/fuelEfficiencies/fuelEfficiencyList', self.index)

      # 차량누적조회
      self.servers['http'].router.add_route('*', '/statusMileages/statusMileageList', self.index)
      self.servers['http'].router.add_route('*', '/statusMileages/statusMileageInsert', self.index)

   # A HTTP handler example
   # More documentation: http://aiohttp.readthedocs.org/en/latest/web.html#handler
   @asyncio.coroutine
   def index(self, request):
      if request.path == '/healthCheckhealthCheck' or request.method == 'OPTIONS':
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
            #  requestDict = dict(post)
            # else:
            #  requestDict = ujson.loads(body)         # json to dict
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
         controllerResult = yield from controllerClass.execute(requestDict, self.daoClass.connection, self.httpClass.connection)

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

      return response

   # Container methods
   @asyncio.coroutine
   def start(self):
      yield from super().start()
      print('server started.')

      try:
         self.daoClass = moduleDao.DaoClass()
         asyncio.async(self.daoClass.open())

         self.httpClass = moduleHttp.HttpClass()
         asyncio.async(self.httpClass.open())
      except:
         print(traceback.format_exc())


   @asyncio.coroutine
   def stop(self):
      try:
         if self.daoClass is not None:
            asyncio.async(self.daoClass.close())

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

