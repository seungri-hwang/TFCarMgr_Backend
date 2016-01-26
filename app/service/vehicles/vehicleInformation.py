import sys
import os
import datetime
import asyncio
from app.data import dataTables

class VehicleInformationClass():
    response = {}

    def __init__(self):
        self.response = {}
        self.currentTime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self.dataTableClass = dataTables.DataTableClass('VL_CAR_INFO')

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

        return self.response

    @asyncio.coroutine
    def create(self, requestDict):
        self.response = requestDict
        try:
            queryCondition = {
                    'method' : 'create'
                ,   'condition' : {
                        'rows' : [{
                            'MM_ID' : requestDict.get('condition').get('mmId'),
                            'VCI_CAR_NUMBER' : requestDict.get('condition').get('carNumber'),
                            'VCI_CAR_NAME' : requestDict.get('condition').get('carName'),
                            'CREATE_DT' : self.currentTime,
                            'UPDATE_DT' : self.currentTime,
                            'DEL_YN' : 'N'
                        }]
                }
            }
            self.response = yield from self.dataTableClass.execute(queryCondition)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def read(self, requestDict):
        self.response = requestDict
        try :
            queryCondition = {
                    'method' : 'read'
                ,   'condition' : {
                        'rows' : [{
                            'VCI_CAR_NUMBER' : requestDict.get('carNumber'),
                            'VCI_ID' : requestDict.get('vciId'),
                            'MM_ID' : requestDict.get('mmId')
                        }]
                }
            }
            self.response = yield from self.dataTableClass.execute(queryCondition)
        except :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

    @asyncio.coroutine
    def update(self, requestDict):
        self.response = {}

        return self.response

    @asyncio.coroutine
    def delete(self, requestDict):
        self.response = requestDict
        try :
            queryCondition = {
                'method' : 'update',
                'condition' : {
                    'rows' : [{
                        'equal' : {
                            'VCI_ID' : requestDict.get('condition').get('vciId')
                        },
                        'DEL_YN' : 'Y'
                    }]
                }
            }
            self.response = yield from self.dataTableClass.execute(queryCondition)
        except :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response