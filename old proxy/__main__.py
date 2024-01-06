__all__ = ['ProxyServer']


from logging import root, DEBUG, basicConfig, debug

for handler in root.handlers[:]:
	root.removeHandler(handler)

basicConfig(
	level=DEBUG,
	filename="session.log",
	filemode="w",
	datefmt="%d-%b-%y %H:%M:%S",
	format="[%(asctime)s]: %(message)s"
)


from enet import Host, Address, ENET_CRC32, Peer, EVENT_TYPE_CONNECT, EVENT_TYPE_RECEIVE, EVENT_TYPE_DISCONNECT, Packet, PACKET_FLAG_RELIABLE
from asyncio import sleep, create_task, run


class ProxyClient:
	def __init__(self, proxy_srv: object, target_hostnport: tuple[str, int]) -> None:
		self.host: Host = Host(
			None,
			1,
			1,
			100_000,
			0,
		)

		self.host.checksum = ENET_CRC32
		self.host.compress_with_range_coder()
		self.peer = self.host.connect(Address(*target_hostnport), 0)

		self.running: bool = False
		self.has_to_restart: bool = False

		self.proxy_srv: Peer = proxy_srv

	async def run(self) -> None:
		self.running = True

		while self.running:
			event = self.host.service(0, True)

			if not event:
				await sleep(0.001)
				continue

			match event.type:
				case int(EVENT_TYPE_CONNECT):
					print("PROXY CLIENT > connected to the server")
				case int(EVENT_TYPE_RECEIVE):
					self.proxy_srv.send(event.packet)
				case int(EVENT_TYPE_DISCONNECT):
					print("PROXY CLIENT > disconnected from the server")
					
					break

	def send(self, packet: Packet) -> None:
		if self.peer:
			self.peer.send(0, packet)

	def stop(self):
		self.running = False

		self.peer.disconnect_now()

		self.host.flush()

		self.host = None
		self.peer = None


from utils import get_hostnport
from growtopia.protocol import *
from growtopia.enums import EventID


class ProxyServer:
	def __init__(self) -> None:
		self.host: Host = Host(Address("127.0.0.1", 10_000), 50)
		self.host.checksum = ENET_CRC32
		self.host.compress_with_range_coder()

		self.game_client_peer: Peer = None
		self.target_host_n_port = None


	async def run(self) -> None:
		proxy_client: ProxyClient = None

		while True:
			event = self.host.service(0, True)

			if not event:
				await sleep(0.001)
				continue

			self.game_client_peer = event.peer

			match event.type:
				case int(EVENT_TYPE_CONNECT):
					debug("GAME CLIENT > connected")
					if proxy_client:
						proxy_client.stop()

					proxy_client = ProxyClient(
						self, self.target_host_n_port or get_hostnport()
					)
					create_task(proxy_client.run())

				case int(EVENT_TYPE_RECEIVE):
					debug("GAME CLIENT: {}".format(event.packet.data))
					if proxy_client:
						proxy_client.send(event.packet)

				case EVENT_TYPE_DISCONNECT:
					debug("GAME CLIENT > disconnected")


	def send(self, packet: Packet) -> None:
		packet_type = Packet.get_type(packet.data)

		if packet_type == PacketType.GAME_UPDATE:
			update_packet = GameUpdatePacket.from_bytes(packet.data)
			event_id = update_packet.identify()

			if event_id == EventID.OnSendToServer:
				variant_list = update_packet.get_variant_list()

				self.target_host_n_port = (
					variant_list.variants[4].value.split("|")[0],
					variant_list.variants[1].value,
				)

				update_packet.variant_list[1].value = 10_000
				update_packet.variant_list[4].value = update_packet.variant_list[
					4
				].value.replace(self.target_host_n_port[0], "127.0.0.1")
				update_packet.set_variant_list(update_packet.variant_list)
				debug(update_packet.serialise())

				self.game_client_peer.send(
					0, Packet(update_packet.serialise(), PACKET_FLAG_RELIABLE)
				)

				debug("PROXY CLIENT > Moving to {}".format(self.target_host_n_port))

				return
			elif event_id == EventID.OnSuperMain:
				debug(packet.data)

		if self.game_client_peer:
			self.game_client_peer.send(0, packet)


if __name__ == '__main__':
	run(ProxyServer().run())