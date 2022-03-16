#!/usr/bin/python3

# ~ This script provides the means to populate database with 
# ~ real-time tickers update emulation

import asyncio
import db


# Clean the database to start demo from scratch
# and ensure the database is properly initialized
db.work_with_db(db.init)


async def spawn():
	"""
	Process running in the background;
	emulate real-time tickers update.
	"""
	while True:
		db.run_tickers()
		await asyncio.sleep(1)


#Running event loop
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = loop.create_task(spawn())
	try:
		loop.run_until_complete(task)
	except KeyboardInterrupt:
		task.cancel()
	except asyncio.CancelledError:
		pass
