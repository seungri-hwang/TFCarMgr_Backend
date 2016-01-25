import asyncio

from app.module import moduleDao, moduleHttp

from app.service import userInformation, userJoin, userLogin

class Controller:
    response = {}

    def __init__(self):
        self.response = {}

    @asyncio.coroutine
    def execute(self, requestDict, daoConnection=None, httpConnection=None):

        #Database Access
        moduleDao.DaoClass.connection = daoConnection
        moduleDao.DaoClass.connection = httpConnection

        try:

            serviceName = requestDict.get('service')
            serviceClass = None

            if serviceName == 'members.memberInsert':
                serviceClass = userJoin.UserJoin()
            elif serviceName == 'members.memberCheckEmail':
                serviceClass = userJoin.UserJoin()
            elif serviceName == 'members.memberList':
                serviceClass = userInformation.UserInformation()
            elif serviceName == 'members.memberEfficiencyInsert':
                serviceClass = userInformation.UserInformation()
            elif serviceName == 'members.memberGet':
                serviceClass = userInformation.UserInformation()
            elif serviceName == 'members.memberLogin':
                serviceClass = userLogin.UserLogin()

            if serviceName is None:
                serviceResult = serviceClass.execute(requestDict)
                self.response = serviceResult
            else:
                self.response = {
                    'isSucceed' : False ,
                    'error' : {
                        'message' : 'You are not authorized to use this service.'
                    }
                }
        except:
            print('[Error] >>>> ', 'File Error!')

        return self.response