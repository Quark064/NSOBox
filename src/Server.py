import asyncio

from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
from http.server import ThreadingHTTPServer
from threading import Thread
from functools import partial

from Hijacker import Hijacker
from Handlers import FRequestHandler

# Configuration
HTTP_SERVER_HOST = "0.0.0.0"
HTTP_SERVER_PORT = 8000

MITM_SERVER_HOST = "0.0.0.0"
MITM_SERVER_PORT = 8080

async def StartMITMProxy(proxy: DumpMaster):
    print("[*] Starting MITM Proxy...")
    await proxy.run()

def ShutdownMITMProxy(proxy: DumpMaster):
    print("[*] Stopping MITM Proxy...")
    proxy.shutdown()

def StartHTTPServer(server: ThreadingHTTPServer):
    print("[*] Starting HTTP Server...")
    server.serve_forever()

def ShutdownHTTPServer(server: ThreadingHTTPServer):
    print("[*] Stopping HTTP Server...")
    server.shutdown()
    server.server_close()

async def main():
    hijack = Hijacker()

    server = ThreadingHTTPServer(
        (HTTP_SERVER_HOST, HTTP_SERVER_PORT),
        lambda *args, **kwargs: FRequestHandler(*args, hijacker=hijack, **kwargs)
    )
    serverThread = Thread(
        target=partial(StartHTTPServer, server),
        daemon=True
    )

    opts = Options(
        listen_host = MITM_SERVER_HOST,
        listen_port = MITM_SERVER_PORT
    )
    proxy = DumpMaster(opts)
    proxy.addons.add(hijack)

    try:
        serverThread.start()
        await StartMITMProxy(proxy)
        
    except asyncio.CancelledError:
        ShutdownHTTPServer(server)
        ShutdownMITMProxy(proxy)
        serverThread.join()

        print("[*] Shutdown Complete!")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    task = loop.create_task(main())

    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        loop.run_until_complete(task)
    finally:
        loop.stop()