from growtopia import Dialog, GameServer, ItemsData, PlayerTribute, DialogElement, Listener, ServerContext


class WorldScanDialog(Dialog):
	def __init__(self, server: GameServer, items_data: ItemsData, player_tribute: PlayerTribute):
		super().__init__("worldscan_dialog")

		self.server = server
		self.items_data = items_data
		self.player_tribute = player_tribute

		self.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_big("World Scan", items_data.get_item("GrowScan 9000").id),
			DialogElement.button("scan_world", "Scan World"),
			DialogElement.ending("worldscan_dialog", "", "")
		)


	@Listener
	async def scan_world(self, ctx: ServerContext) -> None:
		ctx.player.send_log("`oLoading world blocks...")

		# Remove "Scan World" button
		self.elements.pop(2)

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
			self.elements.insert(
				-1,
				DialogElement.smalltext(
					f"`o{name.capitalize()}: `5{value}"
				)
			)

		# Seperator
		self.elements.insert(
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
			self.elements.insert(
				-1,
				DialogElement.label_with_icon_small(
					f"`6{name.capitalize()}`o: `5{amount}",
					self.items_data.get_item(name).id
				)
			)

		ctx.player.send(packet=self.packet)


	@Listener
	async def on_dialog_return(self, ctx: ServerContext) -> None:
		ctx.player.send(packet=ctx.packet)