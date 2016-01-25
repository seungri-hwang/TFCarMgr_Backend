import asyncio

from datetime import datetime
from app.data import dataTables

class UserJoin():
    response = {}

    def __init__(self):
        self.response = {}

    @asyncio.coroutine
    def execute(self, requestDict):
        self.response = requestDict

        try :
            if requestDict['method'] == 'create':
                yield from self.memberInsert(requestDict)
            elif requestDict['method'] == 'read':
                yield from self.memberCheckEmail(requestDict)
        except:
            print('잘못된 요청입니다.')
            pass

        return self.response

    @asyncio.coroutine
    def memberCheckEmail(self, requestDict):
        self.response = requestDict
        return self.response

    @asyncio.coroutine
    def memberInsert(self, requestDict):
        self.response = requestDict

        try:
            databaseMemberObject = dataTables.MemberLayerMember()
            condition = requestDict.get('condition')
            queryCondition = {
                'method' : 'create' ,
                'condition' : {
                    'rows' : [{
                        'MM_USER_EMAIL' : condition.get('userEmail')    ,
                        'MM_USER_NAME' : condition.get('userName')  ,
                        'MM_USER_PASSWORD' : condition.get('userPassword')  ,
                        'CREATE_DT' : datetime.now()
                    }]
                }
            }
            databaseMemberObjectResult = yield from databaseMemberObject.execute(queryCondition)
            self.response = databaseMemberObjectResult
        except:
            self.response = {
                'result' : {
                    'isSucceed' : False,
                    'error' : {
                        'message' : '회원가입에 실패하였습니다.'
                    }
                }
            }
            print('[Error] >>> ', queryCondition)

        return self.response