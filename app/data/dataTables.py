# -*- coding: utf-8 -*-
import sys, os
import asyncio
from app.data import dataTableDispatch

#====================================================================================================
class MemberLayerMember():
	@asyncio.coroutine
	def execute(self, requestDict):
		tableDispatch = dataTableDispatch.DataTableDispatch('ML_MEMBER')
		result = yield from tableDispatch.execute(requestDict)
		return result
#====================================================================================================

#====================================================================================================
class DataStatusSortClass():
	@asyncio.coroutine
	def execute(self, requestDict):
		tableDispatch = dataTableDispatch.DataTableDispatch('SL_STATS_SORT')
		result = yield from tableDispatch.execute(requestDict)
		return result
#====================================================================================================

#====================================================================================================
class DataStatusTypeClass():
	@asyncio.coroutine
	def execute(self, requestDict):
		tableDispatch = dataTableDispatch.DataTableDispatch('SL_STATS_TYPE')
		result = yield from tableDispatch.execute(requestDict)
		return result
#====================================================================================================

#====================================================================================================
'''
class DataBookingFlightCertifiedDocumentClass():

	@asyncio.coroutine
	def execute(self, requestDict):
		tableDispatchClass = dataTableDispatch.DataTableDispathClass('bkBookingFlightCertifiedDocument')
		result = yield from tableDispatchClass.execute(requestDict)
		return result
'''
#====================================================================================================