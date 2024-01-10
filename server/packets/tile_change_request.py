from growtopia import (
    Collection,
    GameServer,
    ItemsData,
    PlayerTribute,
    Listener,
    ServerContext,
    Dialog,
    GameUpdatePacket,
    GameUpdatePacketType,
    GameUpdatePacketFlags,
    VariantList,
)

from random import randint, random


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
        from rich import print as pprint

        pprint("on_tile_change_request: action type: ", ctx.item.action_type)

        # Catch clothing, consumables, ances
        if ctx.item.action_type not in [20, 8, 107]:
            await self.on_tile_place(ctx)

        ctx.world.broadcast(ctx.tile.update_packet)

    @Listener
    async def on_tile_punch(self, ctx: ServerContext) -> None:
        if not ctx.tile.punch():
            return

        if ctx.tile.health <= 0:
            items: dict[int, int] = await self.get_drop_items(ctx.tile.get_layer())

            # break block
            ctx.tile.break_layer()
            ctx.world.broadcast(ctx.tile.update_packet)

            # Drop items
            if items != {}:
                for item_id, amount in items.items():
                    print(
                        f"Spawning {amount}",
                        self.items_data.get_item(item_id).name,
                        end="\n\n",
                    )

                    packet = GameUpdatePacket(
                        update_type=GameUpdatePacketType.ITEM_CHANGE_OBJECT,
                        net_id=-1,
                        vec_x=(ctx.tile.pos[0] * 32.5),
                        vec_y=(ctx.tile.pos[1] * 32.5),
                        int_x=item_id,
                        target_net_id=-1,
                        float_=float(amount),
                        extra_data=b"\x00",
                        extra_data_size=1,
                        flags=[GameUpdatePacketFlags.EXTRA_DATA],
                    )

                    ctx.world.broadcast(packet)

            return

        ctx.world.broadcast(ctx.tile.apply_damage_packet(ctx.player.net_id))

    async def get_drop_items(self, item) -> dict[int, int]:
        items: dict[int, int] = {}

        # Blocks
        if randint(1, 10) == 5:  # 10%
            items[item.id] = 1

        # Seeds
        if randint(1, 4) == 2:  # 25%
            items[item.id + 1] = 1

        # Gems
        if randint(1, 2) == 1:  # 50%
            gems = self.items_data.get_item("gems")
            amount: int = randint(1, 4) * ((item.rarity // 100) + 1)

            items[gems.id] = amount

        return items

    @Listener
    async def on_tile_place(self, ctx: ServerContext) -> None:
        kwargs = {}

        from rich import print as pprint

        print("on_tile_place: ")
        pprint(ctx.item.__dict__)

        # Wrench
        if ctx.item.action_type == 1:
            wrench_dialogs: dict[int, Dialog] = {
                # Door
                2: ctx.server.get_dialog("door_dialog")
            }

            action_type: int = ctx.tile.get_layer().action_type
            dialog: Dialog = wrench_dialogs[action_type]
            setattr(dialog, "_tile_pos", ctx.tile.pos)

            return ctx.player.send(dialog.packet)

        # Doors
        if ctx.item.action_type == 2:
            kwargs["door_label"] = ctx.tile.label

        ctx.tile.set_item(ctx.item, **kwargs)

        ctx.world.broadcast(ctx.tile.update_packet)

        # wrench = 1
        # doors = 2
        # locks = 3
        # gems = 4
        # spikes = 6
        # consumables = 8
        # entrances = 9
        # npcs/sings? = 10
        # jammers = 12
        # bedrock = 15
        # public lava/lava = 16
        # foreground blocks = 17
        # background blocks = 18
        # clothing = 20
        # steam spikes = 45
        # crystals = 56
        # vends = 62
        # automated steam blocks = 69
        # geiger charger = 100
        # ances = 107
        # magplant = 111
        # magplant remote = 112
