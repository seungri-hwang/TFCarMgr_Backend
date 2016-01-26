import asyncio
from app.data import dataTables
import sys,os


class StatusAccountInsert():
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

        # {
        #     "method":"update",
        #     "conditions":
        #     {
        #         "sssID":"1",
        #         "sstID":"1",
        #         "vciID":"1",
        #         "regDate":"2015-05-14",
        #         "priceNum":30500,
        #         "gasNum": 50,
        #         "gasVolumeCd":100,
        #         "distanceNum":4325,
        #         "distanceCd":500,
        #         "gasstationName":"바가지주유소",
        #         "note": "더럽게 비쌈"
        #     }
        # }

        try:
            accountDataMasterClass = dataTables.DataTableClass("SL_STATS_CAR_ACCOUNT")
            conditions = requestDict.get('conditions')
            sscaID = conditions.get('sscaID')
            sssID = conditions.get('sssID')
            vciID = conditions.get('vciID')
            regDate = conditions.get('regDate')
            priceNum = conditions.get('priceNum')
            gasNum = conditions.get('gasNum')
            gasVolumeCd = conditions.get('gasVolumeCd')
            distanceNum = conditions.get('distanceNum')
            distanceCd = conditions.get('distanceCd')
            gasstationName = conditions.get('gasstationName')
            note = conditions.get('note')

            queryCondition = {
                "method": "read_light",
                "conditions": {

                },
                "rows":[{
                    "where": {
                        "SSCA_ID": sscaID
                    }
                }]
            }

            print('---------- rows')
            print(queryCondition)
            retData = yield from accountDataMasterClass.execute(queryCondition)
            list = retData.get('result').get('list')

            # update
            if 0 < len(list):
                print("asdfasdf")

                update = \
                {
                      "SSCA_ID":sscaID,
                      "SSS_ID": sssID,
                      "VCI_ID": vciID,
                      "SSCA_REG_DATE": regDate,
                      "SSCA_PRICE_NUM": priceNum,
                      "SSCA_GAS_NUM": gasNum,
                      "SSCA_GAS_VOLUME_CD": gasVolumeCd,
                      "SSCA_DISTANCE_NUM": distanceNum,
                      "SSCA_DISTANCE_CD": distanceCd,
                      "SSCA_GASSTATION_NAME": gasstationName,
                      "SSCA_NOTE": note
                }

                update['equal'] = {"SSCA_ID":sscaID}

                print("--------------update")
                print( update )

                queryCondition = {
                    "method": "update",
                    "conditions": {
                    }
                }

                retData = yield from accountDataMasterClass.execute(queryCondition)

                print('----------------------- update')
                print(retData)



            # create
            else:
                queryCondition = {

                }




        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)
        return self.response

    @asyncio.coroutine
    def delete(self, requestDict):
        self.response = {}
        return self.response

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}
        return self.response

