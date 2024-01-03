from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Command, ServerContext
from growtopia.enums import NameTitle


class NickCommand(Collection):
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
		

	@Command(name="nick", aliases=["n"])
	async def nick_handler(self, ctx: ServerContext, *, name: str) -> None:
		if len(name) < 5:
			return ctx.player.send_log("`4Minimum player name is 5 letters.")

		await ctx.player.change_name(name)

	
	@Command(name="legendary", aliases=["legend"])
	async def legendary_handler(self, ctx: ServerContext) -> None:
		await ctx.player.add_title(NameTitle.LEGENDARY)


	@Command(name="maxlevel", aliases=["max"])
	async def maxlevel_handler(self, ctx: ServerContext) -> None:
		await ctx.player.add_title(NameTitle.MAX_LEVEL)

	
	@Command(name="doctor", aliases=["doc"])
	async def doctor_handler(self, ctx: ServerContext) -> None:
		await ctx.player.add_title(NameTitle.DOCTOR)


	@Command(name="developer", aliases=["dev"])
	async def admnin_handler(self, ctx: ServerContext) -> None:
		await ctx.player.add_title(NameTitle.DEVELOPER)


	@Command(name="mod")
	async def mod_handler(self, ctx: ServerContext) -> None:
		await ctx.player.add_title(NameTitle.MOD)