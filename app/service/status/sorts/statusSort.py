import sys
import asyncio
from app.data import dataTables

class StatusSortClass():
    response = {}

    def __init__(self):
        self.response = {}

    @asyncio.coroutine
    def execute(self, requestDict):
        self.response = requestDict

        try :
            if requestDict['method'] == 'search':
                yield from self.search(requestDict)
        except :
            pass

        return self.response

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}
        try :
            dataStatusSortClass = dataTables.DataStatusSortClass()
            queryCondition = {
                'method' : 'search',
                'condition' : {
                }
            }
            self.response['result'] = {
				'list': dataStatusSortClass.execute(queryCondition)
			}
        except :
            exc_type = sys.exc_info()
            exc_obj = sys.exc_info()
            exc_tb = sys.exe_info()
            print('[Error] >>> ')

        return self.response['result']

    @asyncio.coroutine
    def create(self, requestDict):
        self.response = {}

    @asyncio.coroutine
    def read(self, requestDict):
        self.response = {}

    @asyncio.coroutine
    def update(self, requestDict):
        self.response = {}

    @asyncio.coroutine
    def delete(self, requestDict):
        self.response = {}