from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext, World, Item, Tile


class GenWorld(Collection):
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
		

	@Command(name="genworld", aliases=["gw"])
	async def handler(self, ctx: ServerContext, *, foreground, background) -> None:
		# Foreground
		foreground: Item | None = self.items_data.get_item(foreground.replace("_", " "))

		if foreground == None:
			foreground: int = 0

		# Background
		background: Item | None = self.items_data.get_item(background.replace("_", " "))

		if background == None:
			background: int = 0
		
		# Generate world
		world: World = ctx.world

		for y in range(world.height // 2, world.height):
			# Base
			ctx.world.set_row_tiles(
				y,
				foreground,
				background
			)

			# Bedrock
			if y >= world.height - 6:
				ctx.world.set_row_tiles(
					y,
					self.items_data.get_item("Bedrock"),
					self.items_data.get_item("Cave Background")
				)
		
		# Main Door
		world.spawn_pos: tuple[int, int] = (50, 29)

		for y in range(world.height):
			for x in range(world.width):
				new_tile = Tile(pos=world.spawn_pos)
				
				# Door
				if (x, y) == world.spawn_pos:
					new_tile.foreground = self.items_data.get_item("Main Door")

				# Bedrock
				if (x, y) == (world.spawn_pos + (0, 1)):
					new_tile.foreground(self.items_data.get_item("Bedrock"))

				ctx.world.tiles[x * y] = new_tile

		# Send to world
		ctx.player.send_to_world(ctx.world)

		# Confirmation message
		ctx.player.send_log("`oGenerated world!")