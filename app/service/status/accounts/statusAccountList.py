import asyncio
from app.data import dataTables
import sys,os


class StatusAccountList():
    response = {}

    def __init__(self):
        self.response = {}
        self.keys = []

    @asyncio.coroutine
    def execute(self,requestDict):
        self.response = requestDict
        try:
            if requestDict['method'] == 'create':
                yield from self.create(requestDict)
            if requestDict['method'] == 'read':
                yield from self.read(requestDict)
            if requestDict['method'] == 'update':
                yield from self.update(requestDict)
            if requestDict['method'] == 'delete':
                yield from self.delete(requestDict)
            if requestDict['method'] == 'search':
                yield from self.search(requestDict)
        except:
            pass

        return self.response


    @asyncio.coroutine
    def create(self, requestDict):
        self.response = {}
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

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}

        try:
            statusDataMaster = dataTables.DataTableClass("SL_STATS_CAR_ACCOUNT")
            condition = requestDict.get("conditions")
            mmID = condition.get("mmID")
            startDt = condition.get("startDt")
            endDt = condition.get("endDt")

            query = u"""
                    SELECT * FROM SL_STATS_CAR_ACCOUNT
                    WHERE (MM_ID = '%s') AND (SSCA_REG_DATE BETWEEN '%s' and '%s')
                    """ % (mmID,startDt,endDt)

            queryCondition = {
                "method":"search",
                "condition": {
                    "query":query
                }
            }

            result = yield from statusDataMaster.execute(queryCondition)

            self.response = result
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response

