from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, Dialog, Item, DialogElement, World


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

		player_clothing = [
			ctx.player.hat,
			ctx.player.chest,
			ctx.player.pants,
			ctx.player.feet,
			ctx.player.face,
			ctx.player.hand,
			ctx.player.back,
			ctx.player.hair,
			ctx.player.neck,
			ctx.player.ances,
			ctx.player.d2,
			ctx.player.d3
		]

		clothing_elements: list[DialogElement] = []
		for clothing in player_clothing:
			item: Item = self.items_data.get_item(clothing)

			if item.id == 0:
				continue

			clothing_elements.append(
				DialogElement.label_with_icon_small(f"`6{item.name} `o(ID: `5{item.id}`o)", item.id)
			)

		print(clothing_elements, end="\n\n")

		dialog.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_big(f"`o{ctx.player.name} `o(Level: `20`o)", self.items_data.get_item("no-face").id),
			DialogElement.smalltext(
				f"`oCurrent Position: `w{str(ctx.player.pos)}"
			),
			DialogElement.smalltext(f"`oCurrent world: `w{world.name}"),
			DialogElement.smalltext(f"`oFloating objects: `w{len(world.objects)}"),
			DialogElement.smalltext(f"`oPlayers in world: `w{len(world.players)}"),
			DialogElement.smalltext("`oClothing:"),
			"\n".join(clothing_elements),
			DialogElement.smalltext(f"`oDays since account was created `w{ctx.player.login_info.player_age}`o, total playtime `w{ctx.player.login_info.totalPlaytime}`o hours."),
			DialogElement.ending("wrench_dialog", "", "")
		)

		ctx.player.send(dialog.packet)