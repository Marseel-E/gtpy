from growtopia import Dialog, GameServer, ItemsData, PlayerTribute, DialogElement, Listener, ServerContext


class DoorDialog(Dialog):
	def __init__(self, server: GameServer, items_data: ItemsData, player_tribute: PlayerTribute):
		super().__init__("door_dialog")

		self.server = server
		self.items_data = items_data
		self.player_tribute = player_tribute

		self.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_big("Door", items_data.get_item("Door").id),
			DialogElement.text_input("door_label", "Label", 20),
			DialogElement.text_input("door_id", "ID", 5),
			DialogElement.text_input("door_destination", "Destination", 21),
			DialogElement.checkbox("door_public", "public", True),
			DialogElement.ending("door_dialog", "Cancel", "Confirm")
		)


	@Listener
	async def on_dialog_return(self, ctx: ServerContext) -> None:
		from rich import pprint
		print("door_dialog:")
		pprint(ctx.packet.__dict__)

		ctx.player.send(packet=ctx.packet)