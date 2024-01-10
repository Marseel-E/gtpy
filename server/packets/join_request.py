from growtopia import (
    Collection,
    GameServer,
    ItemsData,
    PlayerTribute,
    Listener,
    ServerContext,
    World,
    WorldGenerator,
    GameUpdatePacket,
    GameUpdatePacketType,
)


class JoinRequest(Collection):
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
    async def on_join_request(self, ctx: ServerContext) -> None:
        name: str = ctx.packet.arguments.get("name")

        world: World | None = self.server.get_world(name)

        ctx.player.super_moderator = True

        if world == None:
            world = WorldGenerator.default(World(name))

            self.server.add_world(world)

        # [DEBUG] makes the player super moderator
        # ctx.player.super_moderator = True

        # Add the Fist and Wrench to the players inventory
        for item in ["fist", "wrench"]:
            ctx.player.inventory.add_item(self.items_data.get_item(item).id, count=1)

        ctx.player.send_inventory()

        ctx.player.display_name = ctx.player.name

        ctx.player.send_to_world(world)
