from PIL import Image
import json, os

aliases = {
	"bone_block_side": "bone_block",
	"hay_block_side": "hay_block",
	"quartz_block_side": "quartz_block",
	"melon_side": "melon"
}
whitelist = [
	"log",
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
	"block",
	"sponge",
	"melon",
	"prismarine",
	"quartz",
	"bedrock"
]
blacklist = [
	"frosted",
	"mcmeta",
	"door",
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
	"structure",
	"glowstone",
	"campfire",
	"wall",
	"stem",
	"quartz_ore",
	"birch"
]

path = f"{os.path.dirname(os.path.abspath(__file__))}/1.15.2 assets/minecraft/textures/block"
approved = []

# approval process
for file in os.listdir(path):
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
		name = file.replace(".png", "")
		if name in aliases:
			name = aliases[name]

		colors[name] = (int(r/pxCount), int(g/pxCount), int(b/pxCount))

with open(f"{os.path.dirname(os.path.abspath(__file__))}/tileColors.json", "w+", encoding="utf8") as fs:
	json.dump(colors, fs, indent=4)
print(len(colors)) # 102







class DEPRECATED:
	"""
	This is a totally unfeacible way to look up colors
	i don't even know why i thought this would be a good idea
	results generated from this class are stored in allColors.txt which i did you the favor of adding to .gitignore
	"""

	class StoreAllTileMaps:
		# this can be optimized by skipping half of all colors: won't make much difference
		def run():
			print(time.asctime())
			with open(PATH+"/allColors.txt", "a+") as fs:
				with Pool(10) as p: # multiprocessing
					labelList = p.map(StoreAllTileMaps.getBlockUsingMP, StoreAllTileMaps.getCol())
					print(time.asctime())
					last = None
					for color, label in zip(StoreAllTileMaps.getCol(), labelList):
						if label != last: # if the label changes, write the new thing to file
							# store hex values
							r, g, b = tuple(map(lambda i: hex(i)[2:], color))
							# format hex values: 6 -> 06, cd -> cd, f -> 0f
							r, g, b = tuple(map(lambda i: "0"+i if len(i) < 2 else i, (r, g, b)))

							fs.write(f"{r}{g}{b}:{label}" + "\n")
						last = label

		def getBlockUsingMP(rgb):
			return PixelArt.getBlock(*rgb)

		def getCol():
			for r in range(256):
				for g in range(256):
					for b in range(256):
						yield r, g, b