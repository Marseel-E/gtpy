from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, World, WorldGenerator


class TileActivateRequest(Collection):
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
	async def on_tile_activate_request(self, ctx: ServerContext) -> None:
		from rich import print as pprint
		print("tile_activate_request:")
		pprint(ctx.packet.__dict__)

		action_type: int = ctx.item.action_type

		# Wrench
		if action_type == 1:
			print("wrenching some shit\n")

		# Doors
		if action_type == 2:
			destination = "start"

			world: World | None = ctx.server.get_world(destination)

			if world == None:
				world = WorldGenerator.default(World(destination))
				ctx.server.add_world(world)

			ctx.player.send_to_world(world)