from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext, Dialog, DialogElement


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
		dialog = Dialog("worldscan_dialog")

		dialog.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_big("World Scan", self.items_data.get_item("GrowScan 9000").id),
			DialogElement.ending("worldscan_dialog", "", "")
		)

		# Stats
		world_stats: dict[str, int] = {
			"Name": ctx.world.name,
			"Height": ctx.world.height,
			"Width": ctx.world.width,
			"Weather ID": ctx.world.weather_id,
			"Spawn Pos": ctx.world.spawn_pos,
			"Version": ctx.world.version
		}

		for name, value in world_stats.items():
			dialog.elements.insert(
				-1,
				DialogElement.smalltext(
					f"`o{name.capitalize()}: `5{value}"
				)
			)

		# Seperator
		dialog.elements.insert(
			-1,
			DialogElement.spacer_small()
		)

		# Blocks
		world_blocks: dict[str, int] = {}

		for tile in ctx.world.tiles:
			for block in [tile.foreground, tile.background]:
				if block.name not in list(world_blocks.keys()):
					world_blocks[block.name] = 1
					
					continue
				
				world_blocks[block.name] += 1

		for name, amount in world_blocks.items():
			dialog.elements.insert(
				-1,
				DialogElement.label_with_icon_small(
					f"`6{name.capitalize()}`o: `5{amount}",
					self.items_data.get_item(name).id
				)
			)
		
		ctx.player.send(dialog.packet)