from growtopia import (
    Collection,
    GameServer,
    ItemsData,
    PlayerTribute,
    Listener,
    ServerContext,
    GameUpdatePacketFlags,
    GameUpdatePacketType,
    GameUpdatePacket,
)


class StateUpdate(Collection):
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
    async def on_state_update(self, ctx: ServerContext) -> None:
        # Movement packet
        ctx.packet.net_id = ctx.player.net_id

        ctx.world.broadcast(ctx.packet, ctx.player.net_id)
        ctx.player.pos = (ctx.packet.vec_x // 32, ctx.packet.vec_y // 32)

        packet: GameUpdatePacket = GameUpdatePacket(
            update_type=GameUpdatePacketType.SET_CHARACTER_STATE,
            net_id=ctx.player.net_id,
            object_type=23,  # punch id,
            int_=2,  # effect flags (double jump)
            count1=128,  # build range
            count2=128,  # punch range
            target_net_id=24831,  # pupil color
            float_=125.0,  # water speed
            vec_x=1200.0,  # accel
            vec_y=200.0,  # punch strength
            velo_x=310.0,  # speed out
            velo_y=1000.0,  # gravity out
            int_x=-1,  # hair color
            int_y=-1,  # eye color
            extra_data=b"\x00",
            extra_data_size=1,
            flags=[GameUpdatePacketFlags.EXTRA_DATA],
        )

        ctx.player.send(packet)
