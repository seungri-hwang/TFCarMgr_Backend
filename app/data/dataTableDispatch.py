import asyncio

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
            queryCondition = requestDict['condition']
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
                        VALUES (%s)
                        """ % (
                            self.TABLE_NAME,
                            ', '.join([column for column, value in queryConditionRows[0].items()]),
                            ', '.join(['%s' for column, value in queryConditionRows[0].item()])
                        )
                data = []
                for row in queryConditionRows:
                    data += [
                        tuple([value for column, valuye in row.items()])
                    ]

                dictResult = yield from daoClass.executemany(query, data);

                if len(dictResult) > 1:
                    if dictResult.get('error'):
                        result = {
                            'error' : dictResult.get('error')   ,
                            'isSucceed' : False
                        }
                else:
                    result = {
                        'isSucceed' : True
                    }

                    #AI로 생성된 키값은 바로 리턴

                    if dictResult.get('autoIncrement'):
                        result[self.AUTO_INCREMENT] = dictResult.get('autoIncrement')

                self.response['result'] = result
        except:
            print('[Error] >>> 에러입니다')

        return self.response

    @asyncio.coroutine
    def read(self, requestDict):
        return ""

    @asyncio.coroutine
    def update(self, requestDict):
        return ""

    @asyncio.coroutine
    def delete(self, requestDict):
        return ""

    @asyncio.coroutine
    def search(self, requestDict):
        return ""
