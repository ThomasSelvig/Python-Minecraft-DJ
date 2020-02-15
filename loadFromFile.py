# https://github.com/twoolie/NBT
from nbt.nbt import NBTFile
import os, json

class Schematic: # schematics only work in (pre-flattening (before 1.13)) games, due to item ids (schematics use item ids but minecraft doesn't)
	def __init__(self, **kw):
		self.schem = NBTFile(**kw)
		with open(os.path.dirname(os.path.abspath(__file__)) + "/namespaceIdMap.json") as fs:
			self.namespaceIdMap = json.load(fs)


	def blocks(self):
		width, length, height = self.schem["Width"].value, self.schem["Length"].value, self.schem["Height"].value

		for y in range(height):
			for z in range(length):
				for x in range(width):
					index = (y * length + z) * width + x # as described here: https://minecraft.gamepedia.com/Schematic_file_format
					blockId = self.schem["Blocks"].value[index]

					yield {"x": x, "y": y, "z": z, "id": self.namespaceIdMap[str(blockId)]}