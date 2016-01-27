import os
import sys
import asyncio
import traceback

from app.data import dataTableSchema
from app.module import moduleDao

class DataTableDispatchClass():
    response = {}

    def __init__(self, tableName):
        self.response = {}
        self.TABLE_NAME = tableName
        self.AUTO_INCREMENT = dataTableSchema.dbSchema[self.TABLE_NAME]['AUTO_INCREMENT']
        self.COLUMNS = dataTableSchema.dbSchema[self.TABLE_NAME]['COLUMNS']
        self.KEYS = dataTableSchema.dbSchema[self.TABLE_NAME]['KEYS']
        self.NOT_NULL_COLUMNS = dataTableSchema.dbSchema[self.TABLE_NAME]['NOT_NULL_COLUMNS']
        self.SELECT_KEYS = dataTableSchema.dbSchema[self.TABLE_NAME]['SELECT_KEYS']                 # 이건 이해 안감
        self.ADDTIONAL_DATA = dataTableSchema.dbSchema[self.TABLE_NAME]['ADDTIONAL_DATA']           # 이건 이해 안감

    @asyncio.coroutine
    def execute(self, requestDict):
        self.response = {}

        try:
            if requestDict['method'] == 'create':
                yield from self.create(requestDict)
            elif requestDict['method'] == 'read':
                yield from self.read(requestDict)
            elif requestDict['method'] == 'update':
                yield from self.update(requestDict)
            elif requestDict['method'] == 'delete':
                yield from self.delete(requestDict)
            elif requestDict['method'] == 'search':
                yield from self.search(requestDict)
            elif requestDict['method'] == 'read_light':
                yield from self.read_light(requestDict)
        except:
            pass

        return self.response

    @asyncio.coroutine
    def create(self, requestDict):
      self.response = {}
      result = {}

      try:
         daoClass = moduleDao.DaoClass()
         queryCondition = requestDict['condition']
         queryConditionRows = queryCondition.get('rows')
         isValid = len(queryConditionRows) > 0

         errorMessage = ''
         for key, value in queryConditionRows[0].items():
            if key not in self.COLUMNS:
               isValid = False
               errorMessage = '%s is not exists.' % key
               print('Unknown column %s in %s' % (key, self.TABLE_NAME))
               print("----dataTAbleDispatch: "+key)
               break

         if isValid == False:
            # validation error
            result = {
               'isSucceed': False,
               'error': {
                  'message': errorMessage
               }
            }
            self.response['result'] = result
         else:

            query = u"""
                  INSERT INTO %s
                  (%s)
                  values (%s)
               """ % (
               self.TABLE_NAME,
               ', '.join([column for column, value in queryConditionRows[0].items()]),
               ', '.join(['%s' for column, value in queryConditionRows[0].items()])
            )

            print('')
            data = []
            for row in queryConditionRows:

               data += [
                  tuple([value for column, value in row.items()])
               ]

            print("query ----------------")
            print(query)

            dictResult = yield from daoClass.executemany(query, data)

            if len(dictResult) > 1:
               if dictResult.get('error'):
                  result = {
                     'error' : dictResult.get('error'),
                     'isSucceed' : False
                  }
            else:
               result = {
                  'isSucceed': True
               }


         self.response['result'] = result

         print(self.response)
      except:
         exc_type, exc_obj, exc_tb = sys.exc_info()
         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
         print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

      return self.response


    @asyncio.coroutine
    def read_light(self, requestDict):
        self.response = requestDict
        isValid = True
        errorMessage =''
        daoClass = moduleDao.DaoClass()

        try:
            result = {}
            queryCondition = requestDict.get('conditions', {})

            # 필수 값 확인
            for key in self.SELECT_KEYS:
                if not queryCondition.get(key):
                    isValid = False
                    errorMessage = '%s is required column.' % key
                    break

            # 요청한 컬럼이 존재하는지 확인
            for key, value in queryCondition.items():
                if key not in self.COLUMNS:
                    isValid = False
                    errorMessage = 'Unknown column: %s in %s' % (key, self.TABLE_NAME)
                    break

            # 필수 키 값이나 요청한 칼럼이 없다면 에러메시지 리턴 후 모듈 종료
            if isValid == False:
                result = {
                    'isSucceed':False,
                    'error':errorMessage
                }
                self.response['result'] = result
                return self.response

            query = u'SELECT DISTINCT * FROM %s' % self.TABLE_NAME


            # Where절 처리.. like, count 등등은 don't care하고 where만 일단
            rows = requestDict.get('rows')
            if ( 0 < len(rows) ):
                row = rows[0]
                if ( row.get('where') is not None ):
                    where = row.get('where')
                    whereQuery = ""
                    cnt = 0
                    for col in where:
                        if 0 == cnt:
                            whereQuery += "WHERE"
                        elif 0 < cnt:
                            whereQuery += " and "
                        whereQuery += " %s = '%s'" % (col, where.get(col))
                        # print("col:%s, val:%s, cnt:%s  " % (col, where.get(col), cnt))
                        cnt = cnt + 1

            query += " " + whereQuery

            print('print query from dispatch read def-------------------')
            print(query)

            # 개별 query 처리를 허용
            if requestDict.get('query'):
                query = requestDict.get('query')

            # Query 실행
            queryResult = yield from daoClass.execute(query)

            # 결과값 세팅
            result = {
               'isSucceed': True,
               'list': queryResult
             }
            self.response['result'] = result
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}

        try:
            query = requestDict.get('condition').get('query')
            daoClass = moduleDao.DaoClass()
            print('query -----------')
            print(query)
            list = yield from daoClass.execute(query)

            if 0 >= len(list):
                message = "존재하지 않는 테이블입니다."
                result = {
                    "result":False,
                    "message":message
                }
            else:
                message = "성공"
                result = {
                    "result":True,
                    "list":list,
                    "message":message
                }
            self.response = result

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def update(self, requestDict):
        self.response = {}

        try :
            message = None
            dictResult = {}
            queryCondition = requestDict.get('condition')
            queryConditionRows = queryCondition.get('rows')
            daoClass = moduleDao.DaoClass()

            for queryConditionRow in queryConditionRows:
                equal = queryConditionRow.get('equal')

                #쿼리 조건절
                condition = []
                for key in self.KEYS :
                    if queryConditionRow.get('equal'):
                        if equal.get(key):
                            condition.append(u'%s = \'%s\'' % (key, equal.get(key)))

                #정보 입력
                setString = []
                for key, value in queryConditionRow.items():
                    if key not in ('equal'):
                        if value is not None:
                            if type(value) == type(str):
                                value = value.replace('"', "'")
                            setString.append(u'%s = \"%s\"' % (key, value))
                        else :
                            setString.append(u'%s = null' % (key))

            query = u'UPDATE %s \n' % self.TABLE_NAME
            query += u'SET %s \n' % u', '.join(setString)
            query += u' WHERE %s \n' % u' and '.join(condition)

            listDictResult = yield from daoClass.execute(query)

            if len(listDictResult) > 0 :
                if listDictResult.get('error'):
                    message = listDictResult

            if message is not None :
                dictResult['result'] = message
            else :
                dictResult['result'] = {
                    'isSucceed' : True
                }

            self.response = dictResult
        except :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def delete(self, requestDict):
        self.response = {}

        try :
            queryCondition = requestDict.get('condition')
            queryConditionRows = queryCondition.get('rows', [queryCondition])

            for queryConditionRow in queryConditionRows:
                condition = []
                for key in self.KEYS:
                    if queryCondition.get(key):
                        condition.append(u'%s = \'%s\'' % (key, queryConditionRow.get(key)))

                query = u'DELETE FROM %s' % self.TABLE_NAME
                query += u' WHERE %s' % u' and '.join(condition)

                try :
                    daoClass = moduleDao.DaoClass()
                    yield from daoClass.execute(query)
                    result = {
                        'isSucceed' : True
                    }
                except :
                    result = {
                        'isSucceed': False,
                        'error': {
                            'message' : traceback.format_exc()
                        }
                    }
        except :
            result = {
                'isSucceed' : False,
                'error' : {
                    'message' : traceback.format_exc()
                }
            }

        self.response['result'] = result
        return self.response
