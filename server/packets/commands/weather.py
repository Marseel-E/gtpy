from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext


class WeatherCommand(Collection):
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
		

	@Command(name="weather", aliases=["w"])
	async def handler(self, ctx: ServerContext, *, weather_id: int) -> None:		
		ctx.world.weather_id = int(weather_id)
		
		ctx.player.send_to_world(ctx.world)