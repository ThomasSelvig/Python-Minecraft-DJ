import time, random, keyboard as kb, mido, os, json, requests
from PIL import Image
from io import BytesIO

from minecraft.authentication import AuthenticationToken
from minecraft.networking.connection import Connection
# listening for packets, writing packets
from minecraft.networking.packets import clientbound, serverbound
from customPackets import PlayerDiggingPacket
# minecraft datatypes
from minecraft.networking.types import (
    Double, Float, Boolean, VarInt, String, Byte, Position, Enum,
    RelativeHand, BlockFace, Vector, Direction, PositionAndLook,
    multi_attribute_alias
)
'''
build pixelart ingame by using this command as inventoxz:
::PixelArt(url="").buildCanvas(x, y, z)

play music:
add song to queue:
:songname (filename with stripped .mid extension)
play next song in queue:
press PGUP button
skip song / disconnect: F4

move player with (home, delete, end, pgdn) buttons
move player crosshair with arrow keys
'''

class PixelArt:
	COLORS = {
		"white": (0xe9, 0xec, 0xec),
		"orange": (0xf0, 0x76, 0x13),
		"magenta": (0xbd, 0x44, 0xb3),
		"light_blue": (0x3a, 0xaf, 0xd9),
		"yellow": (0xf8, 0xc6, 0x27),
		"lime": (0x70, 0xb9, 0x19),
		"pink": (0xed, 0x8d, 0xac),
		"gray": (0x3e, 0x44, 0x47),
		"light_gray": (0x8e, 0x8e, 0x86),
		"cyan": (0x15, 0x89, 0x91),
		"purple": (0x79, 0x2a, 0xac),
		"blue": (0x35, 0x39, 0x9d),
		"brown": (0x72, 0x47, 0x28),
		"green": (0x54, 0x6d, 0x1b),
		"red": (0xa1, 0x27, 0x22),
		"black": (0x14, 0x15, 0x19)
	}

	def __init__(self, name=None, url=None):
		assert name or url
		im = PixelArt.getImage(name=name) if name else PixelArt.getImage(url=url)
		pixels = im.load()
		alpha = len(pixels[0, 0]) == 4
		
		self.canvas = {
			(x, y): PixelArt.getBlock(
				pixels[x, y][0], 
				pixels[x, y][1], 
				pixels[x, y][2], 
				alpha=pixels[x, y][3] if alpha else None) 
			for x in range(im.size[0]) for y in range(im.size[1])
		}
		# for (x, y), (r, g, b, *_) in pixels.items():
		# 	self.canvas[x, y] = PixelArt.getBlock(r, g, b)

	def buildCanvas(self, ox, oy, oz):
		#ox, oy, oz = pos["x"], pos["y"], pos["z"]

		for (x, y), block in self.canvas.items():
			pixelArtCommands.append(f"/setblock {ox+x} {oy-y} {oz} {block}")


	def getImage(name=None, url=None):
		if url:
			r = requests.get(url)
			try:
				return Image.open(BytesIO(r.content))
			except:
				return None
		else:
			return Image.open(f"{path}/images/{name}.png")


	def getBlock(r, g, b, alpha=None):
		# find closest color using 3d pythagoras. weighted approach since some colors are of less importance
		# when calculating the difference like this, the "sqrt" part is irrelevant
		if alpha == 0:
			return "minecraft:air"

		dc = {}
		for color, (r2, g2, b2) in PixelArt.COLORS.items():
			difference = sum((
				((r2-r)*0.30)**2,
				((g2-g)*0.59)**2,
				((b2-b)*0.11)**2
			))
			dc[difference] = color

		return "minecraft:" + dc[min(dc)] + "_wool"


def setPosition(posPacket):
	global pos
	newValues = {k: v for k, v in posPacket.__dict__.items() if k in ["x", "y", "z", "yaw", "pitch", "flags"]}
	
	if pos:
		pos = {**pos, **newValues}
	else:
		pos = newValues
	
	print("Pos update to client: {x}, {y}, {z}".format(**pos))


def updatePosition(**kwargs):#x=None, y=None, z=None, yaw=None, pitch=None, onGround=None):
	if pos == None and len(kwargs) < 5:
		return None

	packet = serverbound.play.PositionAndLookPacket()

	packet.x		 = pos["x"] if not "x" in kwargs else kwargs["x"]
	packet.feet_y	 = pos["y"] if not "y" in kwargs else kwargs["y"]
	packet.z		 = pos["z"] if not "z" in kwargs else kwargs["z"]
	packet.yaw		 = pos["yaw"] if not "yaw" in kwargs else kwargs["yaw"]
	packet.pitch	 = pos["pitch"] if not "pitch" in kwargs else kwargs["pitch"]
	packet.on_ground = False
	
	dj.write_packet(packet)


def movementControl():
	global pos

	if kb.is_pressed("left"):
		if pos["yaw"] > -180:
			pos["yaw"] -= 1
		else:
			pos["yaw"] = 180

	if kb.is_pressed("right"):
		if pos["yaw"] < 180:
			pos["yaw"] += 1
		else:
			pos["yaw"] = -180

	if kb.is_pressed("down"):
		if pos["pitch"] < 90:
			pos["pitch"] += 1

	if kb.is_pressed("up"):
		if pos["pitch"] > -90:
			pos["pitch"] -= 1
	
	if kb.is_pressed("del"):
		pos["x"] -= .5
	if kb.is_pressed("pgdn"):
		pos["x"] += .5
	if kb.is_pressed("home"):
		pos["z"] -= .5
	if kb.is_pressed("end"):
		pos["z"] += .5


def onChatMessage(packet):
	try:
		if packet.position != 0:
			return None

		data = json.loads(packet.json_data)
		user, msg = data["with"][0]["insertion"], data["with"][1]

		if user != "Inventoxz":
			return None

		if msg.count(":") == 1:
			print("Adding to queue: " + (song := msg[1:]))
			songQueue.append(song)

		elif msg.count(":") == 2:
			exec(msg[2:])

		elif msg.count(":") == 3:
			msg = msg[3:]

			if msg.startswith("left"):
				hand = 0
			elif msg.startswith("right"):
				hand = 1

			dj.write_packet(serverbound.play.AnimationPacket(
				hand=hand
			))


	except Exception as e:
		print("Error in chat event handler: \n" + str(e))


def sendChat(msg):
	dj.write_packet(serverbound.play.ChatPacket(
		message=msg))


def goto(nx, ny, nz):
	amount = 3
	nx, ny, nz = int(nx), int(ny), int(nz)
	# get rounded pos of the bot
	getPos = lambda: tuple(map(lambda i: int(round(i)), (pos["x"], pos["y"], pos["z"])))

	while (p := getPos()) != (nx, ny, nz):
		x, y, z = p
		
		if x < nx:
			x += amount if nx-x >= amount else nx-x
		elif x > nx:
			x -= amount if x-nx >= amount else x-nx

		if y < ny:
			y += amount if ny-y >= amount else ny-y
		elif y > ny:
			y -= amount if y-ny >= amount else y-ny

		if z < nz:
			z += amount if nz-z >= amount else nz-z
		elif z > nz:
			z -= amount if z-nz >= amount else z-nz

		pos["x"], pos["y"], pos["z"] = x, y, z
		print(x, y, z)
		updatePosition()
		time.sleep(0.25)


def playNote(xOffset=0, zOffset=0, tune=None):
	# tune is 0-24 (25 unique noises)
	if tune != None:
		xOffset = tune % 5
		zOffset = tune // 5

	if xOffset < 0 or xOffset > 24 or zOffset < 0 or zOffset > 24:
		return None

	# -2 because player is standing in the middle of the 5x5 array of noteblocks
	# just like pianoTuner()
	location = Position( 
		x=int(round(pos["x"]-2+xOffset)), 
		y=int(round(pos["y"]-1)), 
		z=int(round(pos["z"]-2+zOffset)))
	# start digging
	dj.write_packet(PlayerDiggingPacket(
		status=0, 
		location=location, 
		face=1))
	# cancel digging
	dj.write_packet(PlayerDiggingPacket(
		status=1, 
		location=location, 
		face=1))


def pianoTuner():
	'''
	x x x x x
	x x x x x
	x x o x x
	x x x x x
	x x x x x
	"x" = noteblock
	"o" = player, standing directly on top of a noteblock
	'''

	global pos
	origin = {**pos}
	
	for z in range(5):
		newZ = int(round(origin["z"])) + z - 2
		for x in range(5):
			newX = int(round(origin["x"])) + x - 2

			tune = z*5 + x
			#print("Setting {}, {} to {}".format(newX, newZ, tune))
			for i in range(tune):
				dj.write_packet(serverbound.play.PlayerBlockPlacementPacket(
					hand=0,
					location=Position(x=newX, y=int(pos["y"])-1, z=newZ),
					face=1,
					x=0.5, y=1.0, z=0.5,
					inside_block=False
				))
			time.sleep(0.05)


def playSong(songName, factor=1, scale=False): # scale: put the note into the noteblock range (from midi range: 21-108)
	avail = list(range(54, 54+25)) # if the midi tune is not in this range, it's unavailible in the game

	for msg in mido.MidiFile("midis/"+songName+".mid"):
		time.sleep(msg.time*factor)
		if not msg.is_meta:
			# if not hasattr(msg, "velocity") or msg.velocity == 0:
			# 	# 54-79
			if hasattr(msg, "note") and (scale or msg.note in avail):
				note = msg.note-54 if not scale else int((msg.note-21)/(108-21)*25//1)
				playNote(tune=note)
				
				# bot panic button
				if kb.is_pressed("f4"):
					while kb.is_pressed("f4"):
						pass
					return None


def main():
	# sync time
	old = 0
	while True:
		while (now := time.time()) < old+0.05:
			pass
		old = now
		# time is now synced

		movementControl()

		if len(pixelArtCommands) > 0:
			for i, cmd in enumerate(pixelArtCommands):
				if i != 0 and i % 100 == 0:
					print(f"At index {i}, pausing")
					time.sleep(5) # delay between each 100th block placed
				sendChat(cmd)

			pixelArtCommands.clear()

		if kb.is_pressed("pgup"):# playbutton
			
			if len(songQueue) > 0:
				print("\nCurrently playing:", (songName := songQueue.pop(0)))
				playSong(songName)
				print("Finished: " + songName)
			
			#playSong("thetop")

		if kb.is_pressed("ctrl+shift"):
			pass#playSong("giornostheme", scale=True)

		if kb.is_pressed("f4"):
			exit()
		
		updatePosition()


if __name__ == '__main__':
	# i'm using global vars because pyCraft won't work object oriented ffs
	pos = None
	songQueue = []
	pixelArtCommands = []
	path = os.path.dirname(os.path.abspath(__file__))

	# connect and register listeners
	dj = Connection("127.0.0.1", username="dummy_thicc")
	dj.connect()
	dj.register_packet_listener(setPosition, clientbound.play.player_position_and_look_packet.PlayerPositionAndLookPacket)
	dj.register_packet_listener(onChatMessage, clientbound.play.ChatMessagePacket)
	
	print("Connecting...")
	while pos == None:
		# wait for server to update dj's position
		pass
	print("Connected")
	main()