class UserInformation():
    response = {}

    def __init__(self):
        self.response = {}

    def execute(self, requestDict):
        self.response = requestDict

        try:
            if requestDict['method'] == 'search':
                self.memberList(requestDict)
            elif requestDict['method'] == 'read':
                self.memberGet(requestDict)
            elif requestDict['method'] == 'create':
                self.memberEfficiencyInsert(requestDict)
        except:
            pass
        return self.response

    def memberEfficiencyInsert(self, requestDict):
        return self.response

    def memberGet(self, requestDict):
        return self.response

    def memberList(self, requestDict):
        return self.response