from growtopia import Dialog, GameServer, ItemsData, PlayerTribute, DialogElement, Listener, ServerContext


class GrowIDDialog(Dialog):
	def __init__(self, server: GameServer, items_data: ItemsData, player_tribute: PlayerTribute):
		super().__init__("growid_dialog")

		self.server = server
		self.items_data = items_data
		self.player_tribute = player_tribute

		self.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_small("Get your Grow ID", self.items_data.get_item("Dirt").id),
			DialogElement.text_input("grow_id", "Grow ID", 15),
			DialogElement.text_input("password", "Password", 20),
			DialogElement.spacer_small(),
			DialogElement.text_input("discord", "Discord", 20),
			DialogElement.smalltext("`oYour `wDiscord `owill be used for account verification and support. if you enter a wrong Discord, you can't verify your account, recover or change your password."),
			DialogElement.ending("growid_dialog", "Cancel", "Get My GrowID!")
		)


	@Listener
	async def on_dialog_return(self, ctx: ServerContext) -> None:
		from rich import print as pprint
		print("growid_dialog:")
		pprint(ctx.packet.__dict__)

		ctx.player.send(packet=ctx.packet)