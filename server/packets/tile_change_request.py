from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class TileChangeRequest(Collection):
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
	async def on_tile_change_request(self, ctx: ServerContext) -> None:
		from rich import print as pprint
		pprint(ctx.item.action_type)
		
		# Catch wrench
		if ctx.item.action_type != 1:
			await self.on_tile_place(ctx)

		ctx.world.broadcast(ctx.tile.update_packet)


	@Listener
	async def on_tile_punch(self, ctx: ServerContext) -> None:
		if not ctx.tile.punch():
			return

		if ctx.tile.health <= 0:
			# break block
			ctx.tile.break_layer()
			ctx.world.broadcast(ctx.tile.update_packet)

			return

		ctx.world.broadcast(
			ctx.tile.apply_damage_packet(ctx.player.net_id)
		)

	
	@Listener
	async def on_tile_place(self, ctx: ServerContext) -> None:
		kwargs = {}
		
		# Doors
		if ctx.item.action_type == 2:
			ctx.tile._set_door_extra_data("test_label")

			kwargs["id"] = ""
			kwargs["destination"] = "test"

		ctx.tile.set_item(ctx.item, **kwargs)

		ctx.world.broadcast(ctx.tile.update_packet)

		# foreground blocks = 17
		# background blocks = 18
		# locks = 3
		# doors = 2
		# wrench = 1
		# vends = 62
		# npcs/sings? = 10
		# jammers = 12
		# crystals = 56
		# geiger charger = 100
		# entrances = 9
		# bedrock = 15
		# public lava/lava = 16
		# spikes = 6
		# steam spikes = 45
		# automated steam blocks = 69
		# magplant = 111
		# magplant remote = 112