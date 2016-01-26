import asyncio
import os,sys
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
            elif requestDict['method'] == 'update_light':
                yield from self.update_light(requestDict)
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
         requestUserNo = queryCondition.get('mmID')

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

            # print(query, data)
            dictResult = yield from daoClass.executemany(query, data)
            #print(dictResult)

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
    def update_light(self, requestDict):
        
        self.response = {}
        return self.response

    @asyncio.coroutine
    def update(self, requestDict):
        self.response = {}
        return self.response

    @asyncio.coroutine
    def delete(self, requestDict):
        return ""

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}

        try:
            query = requestDict.get('conditions').get('query')
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
    def read(self, requestDict):
        self.response = requestDict

        try:
            result = {}
            queryCondition = requestDict.get('condition', {})

            # validtion check
            isValid = True
            errorMessage = ''
            calcurateCount = False
            daoClass = moduleDao.DaoClass()

            # 필수 값 확인
            for key in self.SELECT_KEYS:
                if not queryCondition.get(key):
                    isValid = False
                    errorMessage = '%s is required column.' % key
                    break

            # 요청한 컬럼이 존재하는지 확인
            for key, value in queryCondition.items():
                if key not in ('like', 'isNotNull', 'between', 'groupBy', 'isNull', 'lessThan', 'lessThanEqual', 'greaterThan', 'greaterThanEqual', 'equal', 'option', 'limit', 'orderBy', 'orderByDesc', 'or', 'and', 'query'):
                    if key not in self.COLUMNS:
                        isValid = False
                        errorMessage = 'Unknown column: %s in %s' % (key, self.TABLE_NAME)
                        break

            if isValid == False:
                result = {
                    'isSucceed': False,
                    'error': {
                        'message': errorMessage
                    }
                }
            else:
                condition = []

                # generatge query
                for column in self.COLUMNS:
                    if queryCondition.get(column):
                        condition.append(u'`%s` = \'%s\'' % (column, queryCondition.get(column)))

                # like operator
                for likeOperator in queryCondition.get('like', {}):
                    for key, value in likeOperator.items():
                        condition.append(u'`%s` like \'%%%s%%\'' % (key, value) )
                    #condition.append(u'%s like \'%%%s%%\'' % (likeOperator.get('column'), likeOperator.get('value')))

                # between
                if queryCondition.get('between'):
                    for key, value in queryCondition.get('between').items():
                        condition.append(u'`%s` between \'%s\' and \'%s\'' % (key, value[0], value[1]))
                    #value = betweenOperator.get('value')
                    #condition.append(u'%s between \'%s\' and \'%s\'' % (betweenOperator.get('column'), value[0], value[1]))

                # is not null
                for columnName in queryCondition.get('isNotNull', []):
                    condition.append(u'`%s` is not null' % columnName)

                # is null
                for columnNullName in queryCondition.get('isNull', []):
                    condition.append(u'`%s` is null' % columnNullName)

                # less Than
                if queryCondition.get('lessThan'):
                    for key, value in queryCondition.get('lessThan').items():
                        condition.append(u'`%s` < \'%s\'' % (key, value))

                # lessThanEqual
                if queryCondition.get('lessThanEqual'):
                    for key, value in queryCondition.get('lessThanEqual').items():
                        condition.append(u'`%s` <= \'%s\'' % (key, value))

                # greaterThan
                if queryCondition.get('greaterThan'):
                    for key, value in queryCondition.get('greaterThan').items():
                        condition.append(u'`%s` > \'%s\'' % (key, value))

                # greaterThanEqual
                if queryCondition.get('greaterThanEqual'):
                    for key, value in queryCondition.get('greaterThanEqual').items():
                        condition.append(u'`%s` >= \'%s\'' % (key, value))

                # equal
                if queryCondition.get('equal'):
                        for key, value in queryCondition.get('equal').items():
                            condition.append(u'`%s` = \'%s\'' % (key, value))


                # or
                if queryCondition.get('or'):
                    ors = queryCondition.get('or')

                    if type(ors) != type([]):
                        ors = [ors]

                    orCondition = []
                    for __or__ in ors:
                        for key, value in __or__.items():
                            if key == 'and':
                                orAndCondition = []

                                for val in value:
                                    for __key__, __value__ in val.items():
                                        if __value__ == 'is null':
                                            orAndCondition.append(u'`%s` is null' % (__key__))
                                        else:
                                            orAndCondition.append(u'`%s` = \'%s\'' % (__key__, __value__))

                                    orCondition.append(u'(%s)' % ' and '.join(orAndCondition))
                            else:
                                orCondition.append(u'`%s` = \'%s\'' % (key, value))

                    condition.append(u'(%s)' % ' or '.join(orCondition))

                # and
                if queryCondition.get('and'):
                    ands = queryCondition.get('and')

                    if type(ands) != type([]):
                        ands = [ands]

                    andCondition = []
                    for __and___ in ands:
                        for key, value in __and___.items():
                            if key == 'or':
                                andOrCondition = []

                                for val in value:
                                    for __key__, __value__ in val.items():
                                        if __value__ == 'is null':
                                            andOrCondition.append(u'`%s` is null' % (__key__))
                                        else:
                                            andOrCondition.append(u'`%s` = \'%s\'' % (__key__, __value__))

                                    andCondition.append(u'(%s)' % ' or '.join(andOrCondition))
                            elif key == 'orLike':
                                andOrLikeCondition = []

                                for val in value:
                                    for __key__, __value__ in val.items():
                                        andOrLikeCondition.append(u'`%s` like \'%%%s%%\'' % (__key__, __value__))

                                    andCondition.append(u'(%s)' % ' or '.join(andOrLikeCondition))
                            else:
                                andCondition.append(u'`%s` = \'%s\'' % (key, value))

                    condition.append(u'(%s)' % ' and '.join(andCondition))




                query = u'SELECT DISTINCT * FROM %s' % self.TABLE_NAME


                if queryCondition.get('query'):
                    query = queryCondition.get('query')

                if len(condition)> 0:
                    query += u' WHERE %s' % u' and '.join(condition)

                if 'vw' in self.TABLE_NAME:
                    if queryCondition.get('groupBy'):
                        query += u' GROUP BY `%s`' % u'`,`'.join(queryCondition.get('groupBy'))
                    # orderBy
                    if queryCondition.get('orderBy'):
                        query += u' ORDER BY `%s`' % u', '.join(queryCondition.get('orderBy'))
                    elif queryCondition.get('orderByDesc'):
                        query += u' ORDER BY `%s` desc' % u' desc,'.join(queryCondition.get('orderByDesc'))
                else:
                    if queryCondition.get('groupBy'):
                        query += u' GROUP BY %s' % u','.join(queryCondition.get('groupBy'))
                    # orderBy
                    if queryCondition.get('orderBy'):
                        query += u' ORDER BY %s' % u', '.join(queryCondition.get('orderBy'))
                    elif queryCondition.get('orderByDesc'):
                        query += u' ORDER BY %s desc' % u' desc,'.join(queryCondition.get('orderByDesc'))

                # limit
                if queryCondition.get('limit'):
                    limit = queryCondition['limit']
                    query += u' LIMIT %s, %s' % (limit[0], limit[1])


                if queryCondition.get('option'):
                    # 토탈 Count 쿼리 수정 - 15.11.19
                    if queryCondition['option'].get('calcurateCount') == True:
                        calcurateCount = True

                if calcurateCount:
                    (queryResult, total) = yield from daoClass.execute(query, calcurateCount=calcurateCount)
                else:
                    queryResult = yield from daoClass.execute(query)

                timestampColumns = ['firstInsertTime', 'lastUpdateTime', 'approvedCheckedTime', 'settleActionTime', 'cancelActionTime']

                # datetime.date 타입 체크
                if queryCondition.get('option'):
                    if queryCondition.get('option').get('convertDate') == True:
                        for column in queryResult:
                            for key, value in column.items():
                                if type(value) == type(datetime.date(2015, 1, 1)):

                                    # timezone 적용
                                    for timestampColumn in timestampColumns:
                                        if timestampColumn in key:
                                            value = value + datetime.timedelta(hours=9)
                                            break

                                    value = '%s-%02d-%02d' % (value.year, value.month, value.day)
                                    column.update({key: value})

                    #  datetime.datetime 타입 체크
                    if queryCondition.get('option').get('convertDatetime') == True:
                        for column in queryResult:
                            for key, value in column.items():
                                if type(value) == type(datetime.datetime(2015, 1, 1, 1, 1, 1)):

                                    # timezone 적용
                                    for timestampColumn in timestampColumns:
                                        if timestampColumn in key:
                                            value = value + datetime.timedelta(hours=9)
                                            break

                                    value = '%s-%02d-%02d %02d:%02d:%02d' % ( value.year, value.month, value.day, value.hour, value.minute, value.second )
                                    column.update({key: value})


                try:
                    for queryResultRow in queryResult:
                        # firstInsertUno, lastUpdateUno는 항상 변환한다.
                        try:
                            if queryResultRow.get('firstInsertUno'):
                                queryResultRow['firstInsertUnoName'] = yield from redisClass.get('usUserMaster:%s:name' % str(queryResultRow.get('firstInsertUno')))
                            if queryResultRow.get('lastUpdateUno'):
                                queryResultRow['lastUpdateUnoName'] = yield from redisClass.get('usUserMaster:%s:name' % str(queryResultRow.get('lastUpdateUno')))
                        except:
                            pass

                    # ADDTIONAL_DATA
                    if self.ADDTIONAL_DATA:
                        for queryResultRow in queryResult:
                            for addionalDataRow in self.ADDTIONAL_DATA:
                                try:
                                    tableColumnName = addionalDataRow['tableColumnName']

                                    columnEN = None
                                    if addionalDataRow.get('toTransoform'):
                                        toTransoform = addionalDataRow.get('toTransoform')
                                        columnName = toTransoform['columnName']
                                        redisKey = toTransoform['redisKey']

                                        middleKey = ''
                                        lastKey = ''

                                        if len(redisKey) == 2:
                                            middleKey = str(queryResultRow[tableColumnName])
                                            lastKey = redisKey[1]
                                        elif len(redisKey) == 3:
                                            middleKey = redisKey[1]+':'+str(queryResultRow[tableColumnName])
                                            lastKey = redisKey[2]

                                        queryResultRow[columnName] = yield from redisClass.get(redisKey[0]+':'+middleKey+':'+lastKey)
                                        columnEN = queryResultRow[columnName]

                                    if addionalDataRow.get('toTranslate'):
                                        toTranslate = addionalDataRow.get('toTranslate')
                                        extraCode = toTranslate['extraCode']
                                        columnName = toTranslate['columnName']
                                        tableName = toTranslate['tableName']

                                        if columnEN is None:
                                            columnEN = queryResultRow[tableColumnName]

                                        if extraCode != '*':
                                            if extraCode == 'masterCode':
                                                extraCode = queryResultRow['masterCode']
                                            elif extraCode == '[COUNTRY_CODE]':
                                                extraCode = queryResultRow[extraCode][:2]

                                        #print(libMultilingualNameEN, 'KO', tableName,  extraCode)
                                        queryResultRow[columnName] = yield from multilingualClass.execute(columnEN, 'KO', tableName,  extraCode)
                                        if queryResultRow[columnName] is None:
                                            queryResultRow[columnName] = columnEN
                                except:
                                    pass
                except:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

                result = {
                    'isSucceed': True,
                    'list': queryResult
                }

                if calcurateCount == True:
                    result['total'] = total

            self.response['result'] = result
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response


