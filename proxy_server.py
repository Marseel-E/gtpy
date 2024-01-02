from asyncio import run
from proxy import ProxyServer


if __name__ == '__main__':
	run(ProxyServer().run())