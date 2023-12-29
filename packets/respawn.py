from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class Respawn(Collection):
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
	async def on_respawn(self, ctx: ServerContext) -> None:
		print("\n[on_respawn/respawn]:\n", ctx.packet.__dict__, end="\n\n")
		
		ctx.player.kill(respawn=False)
		await ctx.player.freeze(1.5)
		ctx.player.set_pos(*ctx.world.spawn_pos)

	
	@Listener
	async def on_respawn_spike(self, ctx: ServerContext) -> None:
		print("\n[on_respawn_spike/respawn_spike]:\n", ctx.packet.__dict__, end="\n\n")

		ctx.player.kill(respawn=False)
		await ctx.player.freeze(1.5)
		ctx.player.set_pos(*ctx.world.spawn_pos)