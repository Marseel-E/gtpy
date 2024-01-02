from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext, Item


class FindCommand(Collection):
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

		
	@Command(name="find", aliases=["f"])
	async def handler(self, ctx: ServerContext, *, name: str | int = "") -> None:
		if not name:
			return ctx.player.send(
				packet=ctx.server.get_dialog("find_dialog").packet
			)

		item: Item | None = self.items_data.get_item(name)

		if item == None:
			return ctx.player.send_log(f"`4\"`5{name}`4\" not found.")

		ctx.player.add_inventory_item(item.id, 200)

		ctx.player.send_log(f"`oRecieved `5200 {item.name}`o (ID: `5{item.id}`o)!")