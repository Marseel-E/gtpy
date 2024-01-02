__all__ = ['ProxyServer']


import enet
import asyncio

from .utils import get_hostnport
from growtopia.protocol import *
from growtopia.enums import EventID
from .proxy_client import ProxyClient


class ProxyServer:
    def __init__(self) -> None:
        self.host: enet.Host = enet.Host(enet.Address("127.0.0.1", 10_000), 50)
        self.host.checksum = enet.ENET_CRC32
        self.host.compress_with_range_coder()

        self.game_client_peer: enet.Peer = None
        self.target_host_n_port = None

    async def run(self) -> None:
        proxy_client: ProxyClient = None

        while True:
            event = self.host.service(0, True)

            if not event:
                await asyncio.sleep(0.001)
                continue

            self.game_client_peer = event.peer

            match event.type:
                case enet.EVENT_TYPE_CONNECT:
                    print("GAME CLIENT > connected")
                    if proxy_client:
                        proxy_client.stop()

                    proxy_client = ProxyClient(
                        self, self.target_host_n_port or get_hostnport()
                    )
                    asyncio.create_task(proxy_client.run())

                case enet.EVENT_TYPE_RECEIVE:
                    print("GAME CLIENT: {}".format(event.packet.data))
                    if proxy_client:
                        proxy_client.send(event.packet)

                case enet.EVENT_TYPE_DISCONNECT:
                    print("GAME CLIENT > disconnected")

    def send(self, packet: enet.Packet) -> None:
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
                print(update_packet.serialise())

                self.game_client_peer.send(
                    0, enet.Packet(update_packet.serialise(), enet.PACKET_FLAG_RELIABLE)
                )

                print("PROXY CLIENT > Moving to {}".format(self.target_host_n_port))

                return
            elif event_id == EventID.OnSuperMain:
                print(packet.data)
                exit(0)

        # print("PROXY SERVER > {}".format(packet.data[0:250]))

        if self.game_client_peer:
            self.game_client_peer.send(0, packet)
