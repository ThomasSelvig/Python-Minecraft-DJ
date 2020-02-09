from minecraft.networking.types import (
    Double, Float, Boolean, VarInt, String, Byte, Position, Enum,
    RelativeHand, BlockFace, Vector, Direction, PositionAndLook,
    multi_attribute_alias
)
from minecraft.networking.packets import Packet


class PlayerDiggingPacket(Packet):
	@staticmethod
	def get_id(context):
		return 0x1A

	packet_name = "player digging"
	definition = [
		{"status": VarInt},
		{"location": Position},
		{"face": Byte}
	]