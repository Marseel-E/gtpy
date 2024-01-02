from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, Dialog, DialogElement, World, DialogReturn


class Wrench(Collection):
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
	async def on_wrench(self, ctx: ServerContext) -> None:
		dialog = Dialog("wrench_dialog")

		# World info
		world: World | None = ctx.player.world

		if world != None:
			world = ctx.world

		dialog.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_big(f"`o{ctx.player.name} `o(Level: `20`o)", self.items_data.get_item("no-face").id),
			DialogElement.smalltext(
				f"`oCurrent Position: `w{str(ctx.player.pos)}"
			),
			DialogElement.smalltext(f"`oCurrent world: `w{world.name}"),
			DialogElement.smalltext(f"`oFloating objects: `w{len(world.objects)}"),
			DialogElement.smalltext(f"`oPlayers in world: `w{len(world.players)}"),
			DialogElement.smalltext(f"`oDays since account was created `w{ctx.player.login_info.player_age}`o, total playtime `w{ctx.player.login_info.totalPlaytime}`o hours."),
			DialogElement.ending("wrench_dialog", "", "")
		)

		ctx.player.send(dialog.packet)