from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext, Item, GameUpdatePacket, GameUpdatePacketType, VariantList


class SetDCommand(Collection):
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
		

	@Command(name="d")
	async def handler(self, ctx: ServerContext, *, d2: int = 0, d3: int = 0) -> None:

		d2: Item | None = self.items_data.get_item(int(d2))
		d3: Item | None = self.items_data.get_item(int(d3))

		ctx.player.d2 = d2.id if d2 != None else 0
		ctx.player.d3 = d3.id if d3 != None else 0

		print(*ctx.player.get_clothing(), end="\n\n")

		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			net_id=ctx.player.net_id,
			variant_list=VariantList(
				"OnSetClothing",
				*ctx.player.get_clothing()
			)
		)

		ctx.player.send(packet)