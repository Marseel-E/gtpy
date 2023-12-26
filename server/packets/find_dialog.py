from growtopia import Dialog, GameServer, ItemsData, PlayerTribute, DialogElement, Listener, ServerContext, Item

from functools import partial


class FindDialog(Dialog):
	def __init__(self, server: GameServer, items_data: ItemsData, player_tribute: PlayerTribute):
		super().__init__("find_dialog")

		self.server = server
		self.items_data = items_data
		self.player_tribute = player_tribute

		self.add_elements(
			DialogElement.quick_exit(),
			DialogElement.label_with_icon_big("Find", items_data.get_item(name="Magnifying Glass").id),
			DialogElement.text_input("search_bar", "", 30),
			DialogElement.spacer_small(),
			DialogElement.button("search", "Search"),
			DialogElement.spacer_small(),
			DialogElement.ending("find_dialog", "", "")
		)


	async def clean(self) -> None:
		"""
		Removes previous items and/or error text.
		"""
		copy: list[str] = self.elements.copy() # copy the elements
		self.elements.clear() # clear the elements list
		self.elements = copy[:5] + copy[-1:] # remove anything between the core elements (all items and/or error text)


	@staticmethod
	async def _get_item(*args) -> None:
		ctx: ServerContext = args[0]
		item: Item = args[1]

		print("\n\n[find/dialog/get_item]:\n", ctx.packet.__dict__, ctx.packet.identify(), sep="\n", end="\n\n")

		ctx.player.add_inventory_item(item.id, 200)

		ctx.player.send_log(f"`oRecieved `5200 {item.name.capitalize()}`o!")


	@Listener
	async def search(self, ctx: ServerContext) -> None:
		search: str = ctx.packet.arguments.get("search_bar")
		items: list[Item] = self.items_data.get_contains(search)

		if not items:
			self.elements.insert(-1, DialogElement.smalltext(f"`4Couldn't find `5\"{search}\"`4!"))
		else:
			ctx.player.on_console_message("`oLooking for items...")
			
			for item in items:
				if item.name.lower().endswith("seed"):
					continue

				listener_name: str = item.name.lower().replace(" ", "")

				self.elements.insert(-1, DialogElement.button_with_icon(
					listener_name,
					item.name.capitalize(), 
					item.id
				))

				new_handler = partial(
					self._get_item, ctx, item
				)
				setattr(new_handler, "__name__", listener_name)

				self.listener(new_handler)

		ctx.player.send(packet=self.packet)

		await self.clean()


	@Listener
	async def on_dialog_return(self, ctx: ServerContext) -> None:
		ctx.player.send(packet=ctx.packet)