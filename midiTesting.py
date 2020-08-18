import mido

avail = list(range(54, 54+25))

for msg in mido.MidiFile("midis/oldtownroad.mid").play():
	if not msg.is_meta:
		if hasattr(msg, "note") and msg.note in avail:
			note = int((msg.note-21)/(108-21)*25//1)
			print(note)