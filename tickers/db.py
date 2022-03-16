# ~ Database support module,
# ~ describes basic routines
# ~ to interact with the database

import psycopg2
from psycopg2.sql import Identifier, SQL
from multiprocessing import Process, Value
from random import randint
import config


class Ticker:
	"""
	Ticker class, generating movement and storing
	relevant information; supports multiprocessing.
	"""
	
	def __init__(self, n):
		self.id = n
		self.table = f"ticker{self.id}"
		self.val = Value('i', 0)
	
	@staticmethod
	def generate_movement():
		# This version looks less heuristic and more 
		# "math-beautiful" to me :) *blush*
		return 2 * randint(0, 1) - 1
		
	def add(self):
		with self.val.get_lock():
			self.val.value += Ticker.generate_movement()
			
	@property
	def value(self):
		return self.val.value

	def __str__(self):
		return f"Ticker{self.id}"


class Tickers:
	"""
	This class stores created tickers.
	"""
	
	@classmethod
	def clear(cls):
		cls.Tickers = [None] # Index from 1, 1..N
	
	@classmethod
	def new(cls, i):
		cls.Tickers.append(Ticker(i))


def init(db, c):
	"""
	Command to clean and rebuild the database tables,
	creating new Ticker objects along the way. 
	"""
	commands = []
	Tickers.clear()
	for i in range(1, config.TICKERS_COUNT + 1):
		commands.append(f'DROP TABLE IF EXISTS ticker{i};CREATE TABLE ticker{i} (id BIGSERIAL PRIMARY KEY, value INTEGER);')
		Tickers.new(i)
	c.execute('\n'.join(commands))
	db.commit()


def register(db, c):
	"""
	Command to store movement changes of the tickers.
	"""
	c.execute(''.join([
		SQL('INSERT INTO {table} (value) VALUES({value});'.format(
			table=Identifier(ticker.table).as_string(c),
			value=ticker.value,
		)).as_string(c) for ticker in Tickers.Tickers[1:]
	]))
	db.commit()


def export(db, c, ticker, start, finish):
	"""
	Command to load necessary information about pts,
	related to the query.
	"""
	c.execute(f'SELECT value FROM ticker{ticker} WHERE id BETWEEN (%s) AND (%s)', (start, finish))	
	values = [value[0] for value in c.fetchall()]
	return values


def length(db, c, ticker):
	"""
	Command to determind the count of records
	for given ticker.
	"""
	c.execute(f'SELECT COUNT(id) FROM ticker{ticker}')
	return c.fetchone()[0]


def work_with_db(process, *args, **kwargs):
	"""
	Special "shell" for database commands,
	Works as a decorator pattern.
	"""
	result = None
	try:
		connection = psycopg2.connect(
			user=config.DB_USER,
			password=config.DB_PASS,
			host=config.DB_HOST,
			port=config.DB_PORT
		)
		cursor = connection.cursor()
		result = process(connection, cursor, *args, **kwargs)
	except (Exception, psycopg2.Error) as error:
		raise error
	finally:
		if connection:
			cursor.close()
			connection.close()
			return result


def run_tickers():
	"""
	Run process per ticker, then register
	results in the database with a single script.
	"""
	events = []
	for ticker in Tickers.Tickers[1:]:
		e = Process(target=ticker.add)
		events.append(e)
		e.start()
	for event in events:
		event.join()
	work_with_db(register)




if __name__ == '__main__':
	exit()
