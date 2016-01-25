import sys, os
import asyncio
from app.data import dataTables

class MemberEfficiencyClass():
    response = {}

    def __init__(self):
        self.response = {}

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
        self.response = {}
        return self.response

    @asyncio.coroutine
    def create(self, requestDict):
        self.response = requestDict

        try:
            queryCondition = {
                'method' : 'create',
                'condition' : {
                    'rows' : [{
                        'MM_ID' : requestDict.get('mmId'),
                        'CFE_ID' : requestDict.get('cfeId')
                    }]
                }
            }
            dataTableClass = dataTables.DataTableClass('ML_FUEL_EFFICIENCY')
            self.response = dataTableClass.execute(queryCondition)

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

    @asyncio.coroutine
    def read(self, requestDict):
        self.response = {}

    @asyncio.coroutine
    def update(self, requestDict):
        self.response = {}

    @asyncio.coroutine
    def delete(self, requestDict):
        self.response = {}