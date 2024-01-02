from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class GrowID(Collection):
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
	async def on_growid(self, ctx: ServerContext) -> None:
		ctx.player.send(
				packet=ctx.server.get_dialog("growid_dialog").packet
			)