from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, GameUpdatePacket, GameUpdatePacketType, VariantList, GameUpdatePacketFlags

from random import randint


class StateUpdate(Collection):
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
	async def on_state_update(self, ctx: ServerContext) -> None:
		# Set Character State
		packet: GameUpdatePacket = GameUpdatePacket(
			update_type=GameUpdatePacketType.SET_CHARACTER_STATE,
			net_id=ctx.player.net_id
		)

		if GameUpdatePacketFlags.FACING_LEFT in packet.flags:
			packet.flags.remove(GameUpdatePacketFlags.FACING_LEFT)

		ctx.player.send(packet=packet)

		packet.serialise()
		from rich import print as pprint
		pprint("on_state_update:\n", packet.flags, end="\n\n")

		# Clothing update
		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			net_id=ctx.player.net_id,
			variant_list=VariantList(
				"OnSetClothing",
				*ctx.player.get_clothing()
			)
		)

		if GameUpdatePacketFlags.FACING_LEFT in packet.flags:
			packet.flags.remove(GameUpdatePacketFlags.FACING_LEFT)

		ctx.player.send(packet)