import mido

avail = list(range(54, 54+25))

for msg in mido.MidiFile("midis/_oldtownroad.mid").play():
	if not msg.is_meta:
		if hasattr(msg, "note"):# and msg.note in avail:
			print(msg)