import sys
import os
import datetime
import asyncio
from app.data import dataTables

class StatusMileageClass():
    response = {}

    def __init__(self):
        self.response = {}
        self.currentTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.dataTableClass = dataTables.DataTableClass('SL_STATS_MILEAGE')

    @asyncio.coroutine
    def execute(self, requestDict):
        self.response = requestDict

        try :
            if requestDict['method'] == 'search':
                yield from self.search(requestDict)
            if requestDict['method'] == 'create':
                yield from self.create(requestDict)
            if requestDict['method'] == 'read':
                yield from self.read(requestDict)
            if requestDict['method'] == 'update':
                yield from self.update(requestDict)
            if requestDict['method'] == 'delete':
                yield from self.delete(requestDict)
        except :
            pass

        return self.response

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}

        try :
            condition = requestDict.get('condition')
            queryWhere = ''

            if condition.get('vciId') is not None or condition.get('vciId') != '' :
                queryWhere += '''
                    AND VCI_ID = '%s'
                    ''' % condition.get('vciId')

            queryCondition = {
                'method' : 'search',
                'condition' : {
                    'query' :
                        '''
                            SELECT  SSM_DISTANCE_NUM AS distanceNum
                                ,   SSM_DISTANCE_CD AS distanceCd
                            FROM    SL_STATS_MILEAGE
                            WHERE   SSM_ID IS NOT NULL
                            %s
                        ''' % queryWhere
                }
            }

            result = yield from self.dataTableClass.execute(queryCondition)
            self.response['result'] = {
                'list' : result
            }
        except :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def create(self, requestDict):
        self.response = requestDict
        try:
            result = {}
            conditions = requestDict.get('condition')
            queryCondition = {
                'method' : 'create',
                'condition' : {
                    'rows' : [{
                        'VCI_ID' : conditions.get('vciId'),
                        'SSM_DISTANCE_NUM' : conditions.get('distanceNum'),
                        'SSM_DISTANCE_CD' : conditions.get('distanceCd'),
                        'CREATE_DT' : self.currentTime
                    }]
                }
            }
            result = yield from self.dataTableClass.execute(queryCondition)
            self.response = result
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def read(self, requestDict):
        self.response = {}

        return self.response

    @asyncio.coroutine
    def update(self, requestDict):
        self.response = {}

        return self.response

    @asyncio.coroutine
    def delete(self, requestDict):
        self.response = {}

        return self.response