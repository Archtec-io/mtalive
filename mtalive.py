import os
import sys
import logging
import time
import psutil
import asyncio
from aiohttp import web

minetest_running = False
last_check = 0
http_status = 200
check_interval = 15

minetest_path = os.getenv("mtalive_minetest_path")
listening_address = os.getenv("mtalive_listening_address") or "127.0.0.1"
listening_port = os.getenv("mtalive_listening_port") or 3000

log_level = logging.INFO

if minetest_path is None:
	sys.exit("No 'mtalive_minetest_path' environment variable set")

print(f"minetest_path (-e) '{minetest_path}'")
print(f"listening_address (-a) '{listening_address}'")
print(f"listening_port (-p) '{listening_port}'")

def prepare_logging():
	script_path = os.path.dirname(os.path.abspath(__file__))
	log_filename = os.path.join(script_path, "mtalive.log")
	logging.root.handlers = []
	logging.basicConfig(filename = log_filename, level = log_level, format = "%(asctime)s : %(levelname)s : %(funcName)s : %(message)s")
	console = logging.StreamHandler()
	console.setLevel(log_level)
	formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(funcName)s : %(message)s")
	console.setFormatter(formatter)
	logging.getLogger("").addHandler(console)

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
		web.get("/", request_mtalive)
	])
	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, host = listening_address, port = listening_port)
	logging.info("Serving at "+str(listening_address)+":"+str(listening_port))
	await site.start()

try:
	prepare_logging()
	last_check = time.time() - check_interval
	logging.info("Starting mtalive")
	loop = asyncio.get_event_loop()
	loop.create_task(start_server())
	loop.run_forever()
except (KeyboardInterrupt, SystemExit):
	logging.info("Exiting mtalive")
	pass