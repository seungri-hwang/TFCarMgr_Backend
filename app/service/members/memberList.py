import  asyncio
from app.data import dataTables

import sys, os


class MemberListClass():
    response = {}

    def __init__(self):
        self.response = {}
        self.keys = []

    @asyncio.coroutine
    def execute(self, requestDict):
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



    def create(self,requestDict):
        self.response = {}
        return self.response


    def read(self, requestDict):
        self.response = {}

        try:
            dataUserMasterClass = dataTables.DataTableClass("ML_MEMBER")
            dataCarMasterClass = dataTables.DataTableClass("VL_CAR_INFO")
            memberID = requestDict.get('conditions').get('mmID')
            userEmail = requestDict.get('conditions').get('userEmail')

            userQuery = "SELECT * FROM ML_MEMBER"

            userQueryCondition = {
                "method":"read_light",
                "conditions":
                    {
                    },
                "query":userQuery
            }

            list = yield from dataUserMasterClass.execute(userQueryCondition)

            print('------list')
            print(list)

            result = {
                "result": {
                    "isSucceed":True,
                    "list":list
                }
            }
            self.response = result

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)


        return  self.response



    def update(self, requestDict):
        self.response = {}
        return self.response

    def delete(self, requestDict):
        self.response = {}
        return  self.response

    def search(self, requestDict):
        self.response = {}
        return  self.response
