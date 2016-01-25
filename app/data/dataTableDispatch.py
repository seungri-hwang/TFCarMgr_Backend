import asyncio
import os,sys
from app.data import dataTableSchema
from app.module import moduleDao

class DataTableDispatch():
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
        except:
            pass

        return self.response

    @asyncio.coroutine
    def create(self, requestDict):
        self.response = {}
        result = {}

        try:
            daoClass = moduleDao.DaoClass()
            queryCondition = requestDict['conditions']
            queryConditionRows = queryCondition.get('rows')

            isValid = len(queryConditionRows) > 0
            errorMessage = ''


            #Key 값 검증작업
            for key, value in queryConditionRows[0].items():
                if(key not in self.COLUMNS):
                    isValid = False
                    errorMessage = '%s is not exists.' %key

                    break

            if isValid == False:
                result = {
                    'isSucceed' : False ,
                    'error' : {
                        'message' : errorMessage
                    }
                }
            else:
                #쿼리 생성
                query = u"""
                       INSERT INTO %s
                       (%s)
                       values (%s)
                    """ % (
                    self.TABLE_NAME,
                   ', '.join([column for column, value in queryConditionRows[0].items()]),
                   ', '.join(['%s' for column, value in queryConditionRows[0].items()])
                )
                print(query)

                data = []
                for row in queryConditionRows:
                    data += [
                        tuple([value for column, valuye in row.items()])
                    ]

                dictResult = yield from daoClass.executemany(query, data);

                if len(dictResult) > 1:
                    if dictResult.get('error'):
                        result = {
                            'error': dictResult.get('error'),
                            'isSucceed': False
                        }
                else:
                    result = {
                        'isSucceed' : True
                    }

                    if dictResult.get('autoIncrement'):
                        result[self.AUTO_INCREMENT] = dictResult.get('autoIncrement')

                self.response['result'] = result
        except:
            print('[Error] >>> 에러입니다')

        return self.response

    @asyncio.coroutine
    def read(self, requestDict):
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


            # 이후 DB에서 데이터를 read하는 모듈 시작
            condition = []

            for column in self.COLUMNS:
                if queryCondition.get(column):
                    condition.append(u'`%s` = \'%s\'' % (column, queryCondition.get(column)))


            query = u'SELECT DISTINCT * FROM %s' % self.TABLE_NAME

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
    def update(self, requestDict):
        return ""

    @asyncio.coroutine
    def delete(self, requestDict):
        return ""

    @asyncio.coroutine
    def search(self, requestDict):
        return ""
