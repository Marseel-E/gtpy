from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext


class TileChangeRequest(Collection):
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
	async def on_tile_change_request(self, ctx: ServerContext) -> None:
		if ctx.item.action_type in [17, 18, 3]:
			return await self.on_tile_place(ctx)

		ctx.tile.set_item(ctx.item)

		if ctx.item.action_type not in [0, 3, 17, 18]:
			return ctx.player.send_log("`4This action is unhandled!")

		ctx.world.broadcast(ctx.tile.update_packet)


	@Listener
	async def on_tile_punch(self, ctx: ServerContext) -> None:
		if not ctx.tile.punch():
			return

		if ctx.tile.health <= 0:
			# break block
			ctx.tile.break_layer()
			ctx.world.broadcast(ctx.tile.update_packet)

			return

		ctx.world.broadcast(
			ctx.tile.apply_damage_packet(ctx.player.net_id)
		)

	
	@Listener
	async def on_tile_place(self, ctx: ServerContext) -> None:
		ctx.tile.set_item(ctx.item)

		packet = ctx.tile.update_packet

		# locks
		if ctx.item.action_type == 3:
			ctx.tile.foreground = ctx.item.id

			if ctx.item.name in ["small lock", "big lock", "huge lock", "builder's lock"]:
				ctx.tile.lockpos = ctx.tile.pos[0] * ctx.tile.pos[1]

			# extra data
			data = ctx.tile.serialise()

			data += ctx.item.action_type.to_bytes(1, "little") # type
			data += (0).to_bytes(1, "little") # flags
			data += ctx.player.net_id.to_bytes(4, "little") # owner
			data += (0).to_bytes(4, "little") # accessed people = 0
			data += (0).to_bytes(4, "little") # reserved1 = 0
			data += (1).to_bytes(4, "little") # reserved2 = 1

			packet.extra_data = data

		ctx.world.broadcast(packet)