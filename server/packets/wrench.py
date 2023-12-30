from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, GameUpdatePacket


class Wrench(Collection):
	def __init__(
		self,
		server: GameServer,
		items_data: ItemsData,
		player_tribute: PlayerTribute,
	) -> None:
		super().__init__()

		self.server: GameServer = server
		self.items_data: ItemsData = items_data
		self.player_tribute: PlayerTribute = player_tribute


	@Listener
	async def on_wrench(self, ctx: ServerContext) -> None:
		from rich import print as pprint
		print("on_wrench:")
		pprint(ctx.packet.__dict__)

		ctx.player.send(packet=ctx.packet)