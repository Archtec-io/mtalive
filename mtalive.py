import os
import signal
import sys
import logging
import time
import psutil
import asyncio
from aiohttp import web

luanti_running = False
last_check = 0
http_status = 200
check_interval = 10

luanti_path = sys.argv[1]
listening_address = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
listening_port = sys.argv[3] if len(sys.argv) > 3 else 3000

log_level = logging.INFO

if luanti_path is None:
	sys.exit("No 'luanti_path' set")

def signal_term_handler():
	logging.info("Got SIGTERM...")
	asyncio.get_event_loop().stop()

def prepare_logging():
	script_path = os.path.dirname(os.path.abspath(__file__))
	log_filename = os.path.join(script_path, "mtalive.log")
	logging.root.handlers = []
	logging.basicConfig(filename = log_filename, level = log_level, format = "%(asctime)s : %(levelname)s : %(funcName)s : %(message)s")

async def check_process():
	global luanti_running
	global last_check
	global http_status
	logging.debug("Checking processes...")
	last_check = time.time()
	found_luanti = False
	for proc in psutil.process_iter():
		try:
			if proc.exe() == luanti_path:
				found_luanti = True
				luanti_running = True
				http_status = 200
				logging.debug("Found Luanti process.")
				break
		except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
			pass
	if not found_luanti:
		logging.warning("No Luanti process found!")
		luanti_running = False
		http_status = 503

async def request_mtalive(request):
	if time.time() - last_check >= check_interval:
		await check_process()
	return web.Response(text = str(luanti_running).lower()+str("\n"), status = http_status)

async def on_prepare(request, response):
	del response.headers["Server"]

async def start_server():
	app = web.Application()
	app.on_response_prepare.append(on_prepare)
	app.add_routes([
		web.get("/mtalive", request_mtalive)
	])
	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, host = listening_address, port = listening_port)
	logging.info("Serving at "+str(listening_address)+":"+str(listening_port))
	await site.start()

try:
	prepare_logging()
	logging.info(f"luanti_path '{luanti_path}'")
	logging.info(f"listening_address '{listening_address}'")
	logging.info(f"listening_port '{listening_port}'")
	last_check = time.time() - check_interval
	logging.info("Starting mtalive")
	loop = asyncio.new_event_loop()
	loop.add_signal_handler(signal.SIGTERM, signal_term_handler)
	loop.create_task(start_server())
	loop.run_forever()
except (KeyboardInterrupt, SystemExit):
	logging.info("Exiting mtalive")
	pass
