from growtopia import Collection, GameServer, ItemsData, PlayerTribute, Listener, ServerContext, GameUpdatePacket, GameUpdatePacketType, VariantList

from os import walk


class Events(Collection):
	def __init__(
			self,
			server: GameServer,
			items_data: ItemsData,
			player_tribute: PlayerTribute
	) -> None:
		super().__init__()

		self.server: GameServer = server
		self.items_data: ItemsData = items_data
		self.player_tribute: PlayerTribute = player_tribute

	
	@Listener
	async def on_ready(self, _) -> None:
		# Parse data
		await self.items_data.parse()
		await self.player_tribute.parse()

		# Load extensions
		for root, _, files in walk("packets"): # os.walk
			for file in files:
				if file.endswith(".py") and not file.startswith("events"):
					print("loading extension:", file)
					
					self.server.load_extension(
						module_name=file,
						package=root,
						server=self.server,
						items_data=self.items_data,
						player_tribute=self.player_tribute
					)

		print("\nLoaded extensions:", list(self.server.extensions.keys()), end="\n\n")

		# while True:
		# 	items = self.items_data.get_contains(input(">>> "))

		# 	if len(items) < 1:
		# 		continue

		# 	for item in items:
		# 		print(item.clothing_type, item, sep=" | ", end="\n\n")


	@Listener
	async def on_login_request(self, ctx: ServerContext) -> None:
		variant_list = VariantList(
			"OnSuperMainStartAcceptLogonHrdxs47254722215a",
			self.items_data.hash,
			"ubistatic-a.akamaihd.net", # you'd have to fetch that from somewhere
			"0098/787581051/cache/", # you'd have to fetch that from somewhere
			"cc.cz.madkite.freedom org.aqua.gg idv.aqua.bulldog com.cih.gamecih2 com.cih.gamecih com.cih.game_cih cn.maocai.gamekiller com.gmd.speedtime org.dax.attack com.x0.strai.frep com.x0.strai.free org.cheatengine.cegui org.sbtools.gamehack com.skgames.traffikrider org.sbtoods.gamehaca com.skype.ralder org.cheatengine.cegui.xx.multi1458919170111 com.prohiro.macro me.autotouch.autotouch com.cygery.repetitouch.free com.cygery.repetitouch.pro com.proziro.zacro com.slash.gamebuster",
			"proto=189|choosemusic=audio/mp3/about_theme.mp3|active_holiday=0|wing_week_day=0|server_tick=8184975|clash_active=1|drop_lavacheck_faster=1|isPayingUser=1|usingStoreNavigation=1|enableInventoryTab=1|bigBackpack=1|",
			self.player_tribute.hash,
		)

		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			variant_list=variant_list
		)

		ctx.player.send(packet=packet)


	@Listener
	async def on_connect(self, ctx: ServerContext) -> None:
		print(f"{ctx.player.peer.address} has connected to the server!", end="\n\n")

	
	@Listener
	async def on_recieve(self, ctx: ServerContext) -> None:
		print(f"{ctx.player.peer.address} sent a packet with type {ctx.packet._type}")

	
	@Listener
	async def on_disconnect(self, ctx: ServerContext) -> None:
		print(f"{ctx.player.peer.address} has disconnected from the server!")


	@Listener
	async def on_enter_game(self, ctx: ServerContext) -> None:
		variant_list = VariantList(
			"OnRequestWorldSelectMenu", "add_button|Showing: `wRandom Worlds``|_catselect_|0.6|3529161471|\nadd_floater|START|{}|1|3529161471\n"
		)

		packet = GameUpdatePacket(
			update_type=GameUpdatePacketType.CALL_FUNCTION,
			variant_list=variant_list
		)

		ctx.player.send(packet=packet)


	@Listener
	async def on_app_check_response(self, ctx: ServerContext) -> None:
		data: str = ctx.packet.data

		print("[0:on_app_check_response]: ", data if data else "(no-data)", sep="\n", end="\n\n")


	@Listener
	async def on_refresh_item_data(self, ctx: ServerContext) -> None:
		print("[0]: refreshing item data...", end="\n\n")
		ctx.player.send(packet=self.items_data.packet)
		print("[1]: refreshed item data", end="\n\n")


	@Listener
	async def on_refresh_player_tribute_data(self, ctx: ServerContext) -> None:
		print("[0]: refreshing player tribute data...", end="\n\n")
		ctx.player.send(packet=self.player_tribute.packet)
		print("[1]: refreshed player tribute data", end="\n\n")


	@Listener
	async def on_unhandled(self, ctx: ServerContext) -> None:
		print(
			"[1:UNHANDLED]",
			ctx.player.peer.address,
			f"Packet (type: {ctx.packet._type}) data: [{type(ctx.packet.data)}]",
			ctx.packet.data, 
			ctx.packet.__dict__, 
			ctx.packet.identify(), 
			sep="\n", end="\n\n"
		)

	
	@Listener
	async def on_unknown(self, ctx: ServerContext) -> None:
		if not isinstance(ctx.packet, GameUpdatePacket):
			return
		
		if ctx.packet.identify() == "on_unknown":
			return
		
		print("[2:UNKNOWN]", ctx.player.peer.address, f"Packet (type: {ctx.packet._type}) data: [{type(ctx.packet.data)}]", ctx.packet.data, ctx.packet.__dict__, ctx.packet.identify(), sep="\n", end="\n\n")

