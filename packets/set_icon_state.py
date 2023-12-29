from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class SetIcon(Collection):
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
	async def on_set_icon_state(self, ctx: ServerContext) -> None:
		ctx.packet.net_id = ctx.player.net_id		
		ctx.player.send(packet=ctx.packet)