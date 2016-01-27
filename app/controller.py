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
from app.service.status.accounts import statusAccountsInsert,statusAccountList
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
            serviceClass = None

            # 멤버 조인
            if serviceName == 'members.memberInsert':
                serviceClass = memberInsert.MemberInsertClass()
            # 멤버 로그인
            elif serviceName == 'members.memberLogin':
                serviceClass = memberLogin.MemberLoginClass()

            # 멤버 조희
            elif serviceName == 'members.memberGet':
                serviceClass = memberGet.MemberGetClass()

            # 전체회원 조회
            elif serviceName == 'members.memberList':
                serviceClass = memberList.MemberListClass()

            elif serviceName == 'statusTypes.statusTypeList':
                serviceClass = statusType.StatusTypeClass()

            elif serviceName == 'statusSorts.statusSortsList':
                serviceClass = statusSort.StatusSortClass()

            elif serviceName == 'memberEfficiencies.memberEfficiencyInsert':
                serviceClass = memberEfficiency.MemberEfficiencyClass()

            elif serviceName == 'memberEfficiencies.memberEfficiencyGet':
                serviceClass = memberEfficiency.MemberEfficiencyClass()

            elif serviceName == 'vehicles.vehicleInsert':
                serviceClass = vehicleInformation.VehicleInformationClass()

            elif serviceName == 'vehicles.vehicleCheckNumber':
                serviceClass = vehicleInformation.VehicleInformationClass()

            elif serviceName == 'vehicles.vehicleDelete':
                serviceClass = vehicleInformation.VehicleInformationClass()

            elif serviceName == 'fuelEfficiencies.fuelEfficiencyList':
                serviceClass = fuelEfficiency.FuelEfficiencyClass()

            elif serviceName == 'statusMileages.statusMileageList':
                serviceClass = statusMileage.StatusMileageClass()

            elif serviceName == 'statusMileages.statusMileageInsert':
                serviceClass = statusMileage.StatusMileageClass()

            # 차량 주행 상황
            elif serviceName == 'accounts.statusAccountInsert':
                serviceClass = statusAccountsInsert.StatusAccountInsert()

            # 차량 주행 상황 리스트 가져오기
            elif serviceName == 'accounts.statusAccountList':
                serviceClass = statusAccountList.StatusAccountList()

            else:
                serviceResult = {
                    'isSucceed': False,
                    'error': {
                        'message': 'You are not authorized to use this service.'
                    }
                }

            if serviceClass is not None :
                serviceResult = yield from serviceClass.execute(requestDict)

            self.response = serviceResult
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)

        return self.response