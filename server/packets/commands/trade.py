from logging import DEBUG, basicConfig, debug

basicConfig(level=DEBUG)

from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext, GameUpdatePacket, GameUpdatePacketType, VariantList, Player


class TradeCommand(Collection):
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
		

	@Command(name="trade")
	async def handler(self, ctx: ServerContext, name: str) -> None:
		debug(f"trade > Trade initiated with player '{name}'")

		# Get target player
		target_player: Player | None = None
		
		for _, player in ctx.world.players.items():
			if player.name.lower() == name.lower():
				debug("trade > Found target player")
				target_player = player

		# Ensure player is found
		if target_player == None:
			return ctx.player.send_log("`4Player not found!")

		# Send target packet
		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			net_id=target_player.net_id,
			variant_list=VariantList(
				"OnStartTrade",
				ctx.player.name,
				1
			)
		)

		target_player.send(packet)

		debug("trade > Sent target player packet")

		# Send player packet
		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			net_id=ctx.player.net_id,
			variant_list=VariantList(
				f"action|trade_started\nnet_id|{target_player.net_id}"
			)
		)

		ctx.player.send(packet)

		debug("trade > Sent player packet")