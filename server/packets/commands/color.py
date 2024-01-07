from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext


class ColorCommand(Collection):
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


	@Command(name="color", aliases=["c"])
	async def color_handler(self, ctx: ServerContext, r: int, g: int, b: int) -> None:
		# Safe previous color
		color = ctx.player.color

		# Set new color
		ctx.player.color = (r, g, b)

		# Catch invalid colors
		skin: int = ctx.player._get_skin()

		try:
			skin.to_bytes(4, "little", signed=True)
		except OverflowError:
			# Set old color
			ctx.player.color = color
			
			return ctx.player.send_log("`4Invalid color!")


		# Send log message
		ctx.player.send_log(f"`oSet color to `5{skin}`o!")

	
	@Command(name="ghost", aliases=["g"])
	async def ghost_handler(self, ctx: ServerContext) -> None:
		ctx.player.opacity = 255 // 2

		ctx.player.send_log("`oBoOooOOOOoOOO!")