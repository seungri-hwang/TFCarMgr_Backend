import sys, os
import asyncio
from app.data import dataTables

class FuelEfficiencyClass():
    response = {}

    def __init__(self):
        self.response = {}
        self.dataTableClass = dataTables.DataTableClass('CSL_FUEL_EFFICIENCY')

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

            queryCondition = {
                'method' : 'search',
                'condition' : {
                    'query' :
                        '''
                            SELECT  CFE_ID AS cfeId
                                ,   CFE_NAME AS name
                                ,   CFE_EFFCIENCY_CD AS effciencyCd
                                ,   CFE_EXPLANATION_DESC AS explanationDesc
                            FROM    CSL_FUEL_EFFICIENCY
                            WHERE   CFE_ID IS NOT NULL
                            %s
                        ''' % queryWhere
                }
            }

            result = yield from self.dataTableClass.execute(queryCondition)
            self.response['result'] = {
				'list': result
			}
        except :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

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