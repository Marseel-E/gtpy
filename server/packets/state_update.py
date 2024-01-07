from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class StateUpdate(Collection):
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
	async def on_state_update(self, ctx: ServerContext) -> None:
		# Movement packet
		ctx.packet.net_id = ctx.player.net_id

		ctx.world.broadcast(ctx.packet, ctx.player.net_id)