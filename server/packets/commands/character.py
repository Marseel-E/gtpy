from growtopia import Collection, GameServer, ItemsData, PlayerTribute, ServerContext, GameUpdatePacket, GameUpdatePacketType, Command


class CharacterCommands(Collection):
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


	async def send_packet(self, ctx: ServerContext, **kwargs) -> None:
		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.SET_CHARACTER_STATE,
			net_id=ctx.player.net_id,
			**kwargs
		)

		ctx.player.send(packet)

		from rich import print as pprint
		pprint("send_packet:\n", packet.__dict__, end="\n\n")


	@Command(name="punch", aliases=["p"])
	async def punch_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, object_type=int(value))

	
	@Command(name="effect", aliases=["e"])
	async def effect_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, int_=int(value))


	@Command(name="build_range", aliases=["br"])
	async def build_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, count1=int(value))

	
	@Command(name="punch_range", aliases=["pr"])
	async def punch_range_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, count2=int(value))


	@Command(name="pupil", aliases=["pi"])
	async def pupil_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, target_net_id=int(value))


	@Command(name="accel", aliases=["a"])
	async def accel_handler(self, ctx: ServerContext, value: float) -> None:
		await self.send_packet(ctx, vec_x=float(value))

	
	@Command(name="strength", aliases=["s"])
	async def strength_handler(self, ctx: ServerContext, value: float) -> None:
		await self.send_packet(ctx, vec_y=float(value))

	
	@Command(name="hair", aliases=["hc"])
	async def hair_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, int_x=int(value))

	
	@Command(name="eye", aliases=["e"])
	async def eye_handler(self, ctx: ServerContext, value: int) -> None:
		await self.send_packet(ctx, int_y=int(value))