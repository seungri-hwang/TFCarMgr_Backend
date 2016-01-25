import sys, os
import asyncio
# import asyncio_redis
import aioredis
import traceback


class RedisClass():
	host = '127.0.0.1'
	# host = 'redis.travelhow.com'
	port = 6379
	poolsize = 100
	connection = None

	def __init__(self):
		self.tempStoage = {}  # 임시 저장소: 한 클래스내에서 동일한 키 값을 재 조회 되지 않도록 조회한 데이터를 임시로 저장한다.

	@asyncio.coroutine
	def open(self):
		# Create Redis connection

		# if self.connection is None:
		#     self.connection = yield from asyncio_redis.Connection.create(host=self.host, port=self.port)
		# if self.connection is None:
		#     self.connection = yield from aioredis.create_connection((self.host, self.port))
		if RedisClass.connection is None:
			RedisClass.connection = yield from aioredis.create_pool((self.host, self.port), minsize=10, maxsize=1000)
			print('redis opended.')

	@asyncio.coroutine
	def close(self):
		try:
			if RedisClass.connection is not None:
				# RedisClass.connection.clear()
				# RedisClass.connection = None
				# print('redis closed.')
				pass
		except:
			print(traceback.format_exc())

	@asyncio.coroutine
	def set(self, key, value, expire=None, pexpire=None, only_if_not_exists=False, only_if_exists=False):

		yield from self.open()

		try:
			with(yield from RedisClass.connection) as redis:
				yield from redis.set(key, value)
				if expire is not None:
					yield from redis.expire(key, float(expire))

					# yield from self.connection.execute('set', key, value)
					# if expire is not None:
					#     yield from self.connection.execute('expire', key, expire)

					# yield from self.connection.set(key, value)
					# if expire is not None:
					#     yield from self.connection.expire(key, expire)
		except:
			print(traceback.format_exc())

	@asyncio.coroutine
	def get(self, key):

		yield from self.open()

		try:
			if key in self.tempStoage:
				return self.tempStoage[key]
			else:
				with(yield from RedisClass.connection) as redis:
					value = yield from redis.get(key)
					if type(value) == type(b''):
						value = value.decode('utf-8')
					self.tempStoage[key] = value

				# value = yield from self.connection.get(key)
				# if type(value) == type(b''):
				#     value = value.decode('utf-8')

				# try:
				#     value = yield from self.connection.execute('get', key)
				# except:
				#     import traceback
				#     print(traceback.format_exc())
				# if type(value) == type(b''):
				#     value = value.decode('utf-8')

				self.tempStoage[key] = value

				return value
		except:
			print(traceback.format_exc())


	@asyncio.coroutine
	def delete(self, key):
		try:
			with(yield from RedisClass.connection) as redis:
				yield from redis.delete(key)
		except:
			print(traceback.format_exc())