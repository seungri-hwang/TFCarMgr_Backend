# -*- coding: utf-8 -*-
import sys, os
import asyncio
from app.data import dataTableDispatch

#====================================================================================================
class DataTableClass():
	def __init__(self, tableName):
		self.tableName = tableName

	@asyncio.coroutine
	def execute(self, requestDict):
		tableDispatch = dataTableDispatch.DataTableDispatch(self.tableName)
		result = yield from tableDispatch.execute(requestDict)
		return result
#====================================================================================================
