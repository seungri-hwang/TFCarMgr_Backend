import sys, os, datetime
import asyncio
from app.data import dataTables

class StatusMileageClass():
    response = {}

    def __init__(self):
        self.response = {}
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
            if requestDict['method'] == 'put':
                yield from self.update(requestDict)
            if requestDict['method'] == 'delete':
                yield from self.delete(requestDict)
        except :
            pass

        return self.response

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = requestDict
        try :
            queryCondition = {
                'method' : 'search',
                'condition' : {
                    'VCI_ID' : requestDict.get('vciId')
                }
            }
            self.response = self.dataTableClass.execute(queryCondition)
        except :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def create(self, requestDict):
        self.response = requestDict

        try:
            queryCondition = {
                'method' : 'create',
                'condition' : {
                    'rows' : [{
                        'VCI_ID' : requestDict.get('vciId'),
                        'SSM_DISTANCE_NUM' : requestDict.get('distanceNum'),
                        'SSM_DISTANCE_CD' : requestDict.get('distanceCd'),
                        'CREATE_DT' : datetime.datetime()
                    }]
                }
            }

            self.response = self.dataTableClass.execute(queryCondition)
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