# -*- coding: utf-8 -*-

import asyncio
import sys, os

from app.service.members import memberInsert, memberGet, memberList, memberLogin
from app.service.vehicles import vehicleInformation
from app.service.memberEfficiencies import memberEfficiency
from app.service.fuelEfficiencies import fuelEfficiency
from app.service.status.mileages import statusMileage
from app.service.status.sorts import statusSort
from app.service.status.types import statusType
from app.service.status.accounts import statusAccountsInsert
from app.module import moduleDao, moduleHttp


class ControllerClass:
    response = {}

    def __init__(self):
        self.response = {}

    @asyncio.coroutine
    def execute(self, requestDict, daoConnection=None, httpConnection=None):

        moduleDao.DaoClass.connection = daoConnection
        moduleHttp.HttpClass.connection = httpConnection

        try:
            serviceName = requestDict.get('service', '')

            # 멤버 조인
            if serviceName == 'members.memberInsert':
                serviceClass = memberInsert.MemberInsertClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            # 멤버 로그인
            elif serviceName == 'members.memberLogin':
                serviceClass = memberLogin.MemberLoginClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'statusTypes.statusTypeList':
                serviceClass = statusType.StatusTypeClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            # 멤버 조희
            elif serviceName == 'members.memberGet':
                serviceClass = memberGet.MemberGetClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            # 전체회원 조회
            elif serviceName == 'members.memberList':
                serviceClass = memberList.MemberListClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult


            elif serviceName == 'statusSorts.statusSortsList':
                serviceClass = statusSort.StatusSortClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'memberEfficiencies.memberEfficiencyInsert':
                serviceClass = memberEfficiency.MemberEfficiencyClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'memberEfficiencies.memberEfficiencyGet':
                serviceClass = memberEfficiency.MemberEfficiencyClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'vehicles.vehicleInsert':
                serviceClass = vehicleInformation.VehicleInformationClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'vehicles.vehicleCheckNumber':
                serviceClass = vehicleInformation.VehicleInformationClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'vehicles.vehicleDelete':
                serviceClass = vehicleInformation.VehicleInformationClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'fuelEfficiencies.fuelEfficiencyList':
                serviceClass = fuelEfficiency.FuelEfficiencyClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'statusMileages.statusMileageList':
                serviceClass = statusMileage.StatusMileageClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            elif serviceName == 'statusMileages.statusMileageInsert':
                serviceClass = statusMileage.StatusMileageClass()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            # 차량 주행 상황
            elif serviceName == 'accounts.statusAccountInsert':
                serviceClass = statusAccountsInsert.StatusAccountInsert()
                serviceResult = yield from serviceClass.execute(requestDict)
                self.response = serviceResult

            else:
                self.response = {
                    'isSucceed': False,
                    'error': {
                        'message': 'You are not authorized to use this service.'
                    }
                }
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response
