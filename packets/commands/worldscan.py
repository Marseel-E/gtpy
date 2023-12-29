from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext


class WorldScan(Collection):
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

		
	@Command(name="worldscan", aliases=["ws"])
	async def handler(self, ctx: ServerContext) -> None:
		return ctx.player.send(
				packet=ctx.server.get_dialog("worldscan_dialog").packet
			)