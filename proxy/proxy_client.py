__all__ = ['ProxyClient']


import asyncio
import enet


class ProxyClient:
    def __init__(self, proxy_srv: object, target_hostnport: tuple[str, int]) -> None:
        self.host: enet.Host = enet.Host(
            None,
            1,
            1,
            100_000,
            0,
        )

        self.host.checksum = enet.ENET_CRC32
        self.host.compress_with_range_coder()
        self.peer = self.host.connect(enet.Address(*target_hostnport), 0)

        self.running: bool = False
        self.has_to_restart: bool = False

        self.proxy_srv: enet.Peer = proxy_srv

    async def run(self) -> None:
        self.running = True

        while self.running:
            event = self.host.service(0, True)

            if not event:
                await asyncio.sleep(0.001)
                continue

            match event.type:
                case enet.EVENT_TYPE_CONNECT:
                    print("PROXY CLIENT > connected to the serve")
                case enet.EVENT_TYPE_RECEIVE:
                    self.proxy_srv.send(event.packet)
                case enet.EVENT_TYPE_DISCONNECT:
                    print("PROXY CLIENT > disconnected from the server")
                    break

    def send(self, packet: enet.Packet) -> None:
        if self.peer:
            self.peer.send(0, packet)

    def stop(self):
        self.running = False

        self.peer.disconnect_now()

        self.host.flush()

        self.host = None
        self.peer = None
