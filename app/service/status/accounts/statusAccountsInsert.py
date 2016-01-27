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

        try:
            accountDataMasterClass = dataTables.DataTableClass("SL_STATS_CAR_ACCOUNT")
            conditions = requestDict.get('conditions')
            sstID = conditions.get('sstID')
            sssID = conditions.get('sssID')
            vciID = conditions.get('vciID')
            mmID = conditions.get('mmID')
            regDate = conditions.get('regDate')
            priceNum = conditions.get('priceNum')
            gasNum = conditions.get('gasNum')
            gasVolumeCd = conditions.get('gasVolumeCd')
            distanceNum = conditions.get('distanceNum')
            distanceCd = conditions.get('distanceCd')
            gasstationName = conditions.get('gasstationName')
            note = conditions.get('note')

            print("mmID: %s" %  mmID)

            rows = {
                "SST_ID": sstID,
                "SSS_ID": sssID,
                "VCI_ID": vciID,
                "MM_ID": mmID,
                "SSCA_REG_DATE": regDate,
                "SSCA_PRICE_NUM": priceNum,
                "SSCA_GAS_NUM": gasNum,
                "SSCA_GAS_VOLUME_CD": gasVolumeCd,
                "SSCA_DISTANCE_NUM": distanceNum,
                "SSCA_DISTANCE_CD": distanceCd,
                "SSCA_GASSTATION_NAME": gasstationName,
                "SSCA_NOTE": note
            }
            queryCondition = {
                "method": "create",
                "condition": {
                    "rows": [rows]
                }
            }
            result = yield from accountDataMasterClass.execute(queryCondition)
            self.response = result
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

