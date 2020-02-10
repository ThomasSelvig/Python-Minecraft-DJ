from PIL import Image
from os import listdir
import json

whitelist = [
	"planks",
	"concrete",
	"terracotta",
	"wool",
	"wood",
	"ice",
	"bricks",
	"clay",
	"stone",
	"dirt",
	"andesite",
	"granite",
	"diorite",
	"block"
]
blacklist = [
	"mcmeta",
	"grass_block",
	"stairs",
	"slab",
	"stage",
	"dust",
	"glazed",
	"command",
	"powder",
	"coral",
	"grindstone",
	"honey",
	"mushroom",
	"_bottom",
	"_top",
	"_on",
	"torch",
	"stonecutter",
	"structure"
]

path = "C:/Users/Thomas/AppData/Roaming/.minecraft/versions/1.15.1/assets/minecraft/textures/block"
approved = []

# approval process
for file in listdir(path):
	blacklisted = any([term in file for term in blacklist])
	whitelisted = any([term in file for term in whitelist])

	if whitelisted and not blacklisted:
		approved.append(file)

colors = {}
for file in approved:
	im = Image.open(path+"/"+file)
	px = im.load()

	# if not grayscale
	if type(px[0, 0]) != int and len(px[0, 0]) >= 3:

		r, g, b = 0, 0, 0
		for y in range(im.size[1]):
			for x in range(im.size[0]):
				p = px[x, y]
				r += p[0]
				g += p[1]
				b += p[2]

		pxCount = im.size[0]*im.size[1]
		colors[file.replace(".png", "")] = (r/pxCount, g/pxCount, b/pxCount)

print(json.dumps(colors, indent=4))