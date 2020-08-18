# Python Minecraft DJ
 Minecraft client with the purpose of playing midi-songs on noteblocks! \
 The bot is purely CLI and works by directly sending network packets thru the python library pyCraft (a python implementation of the [minecraft protocol](https://wiki.vg/Protocol). \
 The bot also does pixelart, as seen in the background of the video-demo below.

## Demo of the music-part of the bot
https://youtu.be/-EztfmSk8MQ

## The noteblock range
The noteblocks in minecraft only cover 25 notes (for multiple instruments)
The bot (dummy_thicc) works by reading midi files and converting the midi note to a range on a board of noteblocks, which it uses to punch a correct note. \
Some notes are too high for the bot to play on a noteblock: In that case, the note isn't played at all.

![piano_range](https://github.com/ThomasSelvig/Python-Minecraft-DJ/blob/master/pianorange.png)
