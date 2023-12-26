from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, GameUpdatePacket, GameUpdatePacketType, VariantList, Colour


class Input(Collection):
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
	async def on_input(self, ctx: ServerContext) -> None:
		text: str = ctx.packet.arguments.get("text", None)
		
		# text bubble
		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			variant_list=VariantList(
				"OnTalkBubble", ctx.player.net_id,
				text,
			)
		)

		ctx.player.send(packet=packet)

		# chat text
		ctx.player.on_console_message(f"[{Colour.WHITE + ctx.player.name}`o]: {Colour.WHITE + text}")