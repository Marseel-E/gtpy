from growtopia import GameServer, ItemsData, PlayerTribute


class Server(GameServer):
	def __init__(
		self, 
		host: str, 
		port: int
	) -> None:
		super().__init__((host, port))

		self.load_extension(
			"events",
			"packets",
			server=self,
			items_data=ItemsData("data/items.dat"),
			player_tribute=PlayerTribute("data/player_tribute.dat")
		)

		print("Main Loaded Extensions:", list(self.extensions.keys()), end="\n\n")


if __name__ == '__main__':
	from asyncio import run


	server = Server("127.0.0.1", 10_000)
	run(server.run())