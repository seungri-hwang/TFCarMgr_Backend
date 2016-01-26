import asyncio
from app.data import dataTables
import sys,os


class MemberLoginClass():
    response = {}

    def __init__(self):
        self.response = {}
        self.keys = []

    @asyncio.coroutine
    def exccute(self,requestDict):
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

        try:
            dataUserMasterClass = dataTables.DataTableClass("ML_MEMBER")
            memberEmail = requestDict.get("conditions").get("userEmail")
            memberPassword = requestDict.get("conditions").get("userPassword")
            memberID = ""

            query = "SELECT MM_USER_PASSWORD,MM_ID FROM ML_MEMBER WHERE MM_USER_EMAIL = '%s'" % memberEmail

            queryCondition = {
                "method":"read_light",
                "conditions":
                    {
                        "MM_USER_PASSWORD" : memberPassword,
                        "MM_USER_EMAIL": memberEmail
                    },
                "query":query
            }

            list = yield from dataUserMasterClass.execute(queryCondition)

            # 없는 회원
            if 0 >= len(list.get('result').get('list')):
                print("------ read Fail")
                message = "존재하지 않는 회원입니다."
                result = {
                    "isSucceed": False,
                    "messgae": message
                }

            else:
                retData = list.get('result').get('list')[0]

                memberID = retData.get("MM_ID")
                retPass = retData.get("MM_USER_PASSWORD")

                # 패스워드 오류
                if memberPassword != retPass:
                    message = "패스워드가 틀렸습니다. 다시 입력해주세요."
                    result = {
                        "isSucceed": False,
                        "messgae": message
                    }
                # 패스워드 일치(로그인 완료)
                else:
                    result = list

                    # 정보를 뿌려준다?
                self.response = result
        except:
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
        self.response = {}
        return self.response

    @asyncio.coroutine
    def search(self, requestDict):
        self.response = {}
        return self.response


