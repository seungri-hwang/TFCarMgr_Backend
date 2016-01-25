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
class DataMemberMasterClass():

   @asyncio.coroutine
   def execute(self, requestDict):
      tableDispatchClass = dataTableDispatch.DataTableDispathClass('ML_MEMBER')
      result = yield from tableDispatchClass.execute(requestDict)
      return result
#====================================================================================================