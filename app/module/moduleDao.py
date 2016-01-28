# -*- coding: utf-8 -*-

import aiomysql
import asyncio
import time
import traceback
from app.config import database

# import pymysql

class DaoClass():
	host = database.database.get('host')
	user = database.database.get('user')
	password = database.database.get('password')
	db = database.database.get('db')
	'''
	# host = 'db.travelhow.com'
	host = 'devdb.travelhow.com'

	user = 'travelhow'
	password = 'port8812!!#'
	db = 'TFCarMgr'
	'''

	connection = None

	def __init__(self):
		pass


	@asyncio.coroutine
	def open(self):
		if DaoClass.connection is None:
			# DaoClass.connection = yield from aiomysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8mb4')
			# DaoClass.connection = yield from aiomysql.create_pool(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8mb4', minsize=5, maxsize=10, autocommit=True)
			DaoClass.connection = yield from aiomysql.create_pool(host=self.host, user=self.user, password=self.password, db=self.db, charset='utf8mb4', minsize=5, maxsize=1000, autocommit=True)
			print('db opended.')

			# DaoClass.connection = pymysql.connect(host=self.host, port=3306, user=self.user, passwd=self.password, db=self.db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
			# DaoClass.connection.autocommit(True)

	@asyncio.coroutine
	def close(self):
		if DaoClass.connection is not None:
			DaoClass.connection.close()
			DaoClass.connection = None
			print('db closed.')

	@asyncio.coroutine
	def execute(self, query, calcurateCount=False):
		timeBegin = time.time()

		dictResult = {}
		totalCount = 0

		# QUERY = query.upper()
		errorMessage = ''
		errorStatus = False

		yield from self.open()
		# self.open()

		try:
			# cursor = yield from DaoClass.connection.cursor(aiomysql.DictCursor)

			cursor = None
			with(yield from DaoClass.connection) as conn:
				cursor = yield from conn.cursor(aiomysql.DictCursor)

				yield from cursor.execute(query)
				dictResult = yield from cursor.fetchall()

				if calcurateCount:
					yield from cursor.execute('SELECT FOUND_ROWS() as totalCount;')
					dictResult2 = yield from cursor.fetchone()
					totalCount = dictResult2['totalCount']

			# cursor = DaoClass.connection.cursor()
			# cursor.execute(query)
			# dictResult = cursor.fetchall()
			#
			# if calcurateCount:
			# 	cursor.execute('SELECT FOUND_ROWS() as totalCount;')
			# 	dictResult2 = cursor.fetchone()
			# 	totalCount = dictResult2['totalCount']

			# cursor.close()
		except:
			# if 'INSERT INTO' in QUERY or 'UPDATE ' in QUERY or 'DELETE ' in QUERY:
			# 	yield from DaoClass.connection.rollback()

			errorMessage = traceback.format_exc()
			errorStatus = True

			# 에러 처리.
			# exc_type, exc_obj, exc_tb = sys.exc_info()
			# fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			# print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)
			print(errorMessage)

		if errorStatus == True:
			dictResult['isSucceed'] = False
			dictResult['error'] = {
				'message' : errorMessage
			}

		# print(dictResult)
		# self.close()
		# print('moduleDao.execute :', time.time() - timeBegin)

		if calcurateCount:
			return (dictResult, totalCount)
		else:
			return dictResult

	@asyncio.coroutine
	def executemany(self, query, data):
		timeBegin = time.time()

		dictResult = {}
		QUERY = query.upper()
		errorMessage = ''
		errorStatus = False

		yield from self.open()
		# self.open()

		try:
			# cursor = yield from DaoClass.connection.cursor(aiomysql.DictCursor)

			cursor = None
			with(yield from DaoClass.connection) as conn:
				cursor = yield from conn.cursor(aiomysql.DictCursor)

				yield from cursor.executemany(query, data)
				dictResult = yield from cursor.fetchall()

				# if 'INSERT INTO' in QUERY or 'UPDATE ' in QUERY or 'DELETE ' in QUERY:
				# 	yield from DaoClass.connection.commit()

				lastRowId = cursor.lastrowid
				if lastRowId is not None:
					dictResult = {
						'autoIncrement' : lastRowId
					}

			# cursor = DaoClass.connection.cursor()
			# cursor.executemany(query, data)
			# dictResult = cursor.fetchall()
			#
			# lastRowId = cursor.lastrowid
			# if lastRowId is not None:
			# 	dictResult = {
			# 		'autoIncrement' : lastRowId
			# 	}

			# cursor.close()
		except:
			# if 'INSERT INTO' in QUERY or 'UPDATE ' in QUERY or 'DELETE ' in QUERY:
			# 	yield from DaoClass.connection.rollback()

			errorMessage = traceback.format_exc()
			errorStatus = True

			# 에러 처리.
			# exc_type, exc_obj, exc_tb = sys.exc_info()
			# fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			# print('[Error] >>>> ', exc_type, fname, exc_tb.tb_lineno)
			print(errorMessage)

		if errorStatus == True:
			dictResult['isSucceed'] = False
			dictResult['error'] = {
				'message' : errorMessage
			}

		# self.close()

		# print('moduleDao.executemany :', time.time() - timeBegin)

		return dictResult