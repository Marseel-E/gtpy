from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, GameUpdatePacket, GameUpdatePacketType, VariantList


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
		print(ctx.item.bodypart, ctx.item.clothing_type, ctx.item.action_type, ctx.item.category, ctx.item.kind, ctx.item, end="\n\n", sep=" <> ")

		item_id: int = ctx.item.id
		name: list[str] = ctx.item.name.split(' ')
		print(name, end="\n\n")

		match ctx.item.clothing_type:
			case 0: # hat
				ctx.player.hat = item_id
			case 1: # chest
				ctx.player.chest = item_id
			case 2: # pants
				ctx.player.pants = item_id
			case 3: # feet
				ctx.player.feet = item_id
			case 4: # face
				ctx.player.face = item_id
			case 5: # hand
				if "Ancestral" in name:
					ctx.player.ances = item_id
				else:
					ctx.player.hand = item_id
			case 6: # back
				if "Ancestral" in name:
					ctx.player.ances = item_id
				else:
					ctx.player.back = item_id
			case 7: # hair
				ctx.player.hair = item_id
			case 8: # neck
				ctx.player.neck = item_id

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