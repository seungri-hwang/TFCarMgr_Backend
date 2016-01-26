import asyncio
from app.data import dataTables

import sys, os


class MemberGetClass():
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

            userQuery = "SELECT MM_USER_NAME,MM_USER_EMAIL FROM ML_MEMBER WHERE MM_ID = '%s' and MM_USER_EMAIL='%s'" % (memberID,userEmail)

            userQueryCondition = {
                "method":"read_light",
                "conditions":
                    {
                        "MM_ID" : memberID,
                        "MM_USER_EMAIL": userEmail
                    },
                "query":userQuery
            }

            userList = yield from dataUserMasterClass.execute(userQueryCondition)

            carQuery = "SELECT VCI_ID, VCI_CAR_NUMBER, VCI_CAR_NAME FROM VL_CAR_INFO  WHERE MM_ID = '%s'" % memberID

            carQueryCondition = {
                "method":"read_light",
                "conditions":
                    {
                        "MM_ID" : memberID
                    },
                "query":carQuery
            }

            carList = yield from dataCarMasterClass.execute(carQueryCondition)

            if 0 >= len(userList.get('result').get('list')) or 0 >= len(carList.get('result').get('list')):
                result = {
                    "result": {
                        "isSucceed":False,
                        "message":"데이터가 존재하지 않습니다"
                    }
                }
                self.response = result

            else:
                uList = userList.get('result').get('list')[0]
                cList = carList.get('result').get('list')[0]

                list = {}

                for key, val in uList.items():
                    list.__setitem__(key, val)

                for key, val in cList.items():
                    list.__setitem__(key, val)


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
