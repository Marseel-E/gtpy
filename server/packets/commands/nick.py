from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext


class NickCommand(Collection):
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
		

	@Command(name="nick", aliases=["n"])
	async def handler(self, ctx: ServerContext, *, name: str) -> None:		
		ctx.player.display_name = name

		ctx.player.send_to_world(ctx.world)