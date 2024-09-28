import os
import signal
import sys
import logging
import time
import psutil
import asyncio
from aiohttp import web

minetest_running = False
last_check = 0
http_status = 200
check_interval = 10

minetest_path = sys.argv[1]
listening_address = sys.argv[2] or "127.0.0.1"
listening_port = sys.argv[3] or 3000

log_level = logging.INFO

if minetest_path is None:
	sys.exit("No 'minetest_path' set")

def signal_term_handler():
    logging.info("Got SIGTERM...")
    sys.exit(0)

def prepare_logging():
	script_path = os.path.dirname(os.path.abspath(__file__))
	log_filename = os.path.join(script_path, "mtalive.log")
	logging.root.handlers = []
	logging.basicConfig(filename = log_filename, level = log_level, format = "%(asctime)s : %(levelname)s : %(funcName)s : %(message)s")

async def check_process():
	global minetest_running
	global last_check
	global http_status
	logging.debug("Checking processes...")
	last_check = time.time()
	found_minetest = False
	for proc in psutil.process_iter():
		try:
			if proc.exe() == minetest_path:
				found_minetest = True
				minetest_running = True
				http_status = 200
				logging.debug("Found Minetest process.")
				break
		except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
			pass
	if not found_minetest:
		logging.warning("No Minetest process found!")
		minetest_running = False
		http_status = 503

async def request_mtalive(request):
	if time.time() - last_check >= check_interval:
		await check_process()
	return web.Response(text = str(minetest_running).lower()+str("\n"), status = http_status)

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
	logging.info(f"minetest_path '{minetest_path}'")
	logging.info(f"listening_address '{listening_address}'")
	logging.info(f"listening_port '{listening_port}'")
	last_check = time.time() - check_interval
	logging.info("Starting mtalive")
	loop = asyncio.get_event_loop()
	loop.add_signal_handler(signal.SIGTERM, signal_term_handler)
	loop.create_task(start_server())
	loop.run_forever()
except (KeyboardInterrupt, SystemExit):
	logging.info("Exiting mtalive")
	pass