from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext


class HelpCommand(Collection):
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
		

	@Command(name="help", aliases=["?"])
	async def handler(self, ctx: ServerContext) -> None:		
		text: str = "`oCommands: "

		commands: list[str] = ctx.server.commands.keys()

		for i, command in enumerate(commands):
			text += f"`#/{command}`o, "

			if (i + 1) == len(commands):
				text = text[:-2]

		ctx.player.send_log(text)