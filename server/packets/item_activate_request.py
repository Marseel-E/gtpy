from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class ItemActivateRequest(Collection):
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
	async def on_item_activate_request(self, ctx: ServerContext) -> None:
		from rich import print as pprint
		print("item_activate_request:")
		pprint(ctx.tile.update_packet.__dict__)