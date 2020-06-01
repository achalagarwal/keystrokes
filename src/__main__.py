from stream import FileSource
from stream import return_corrected_pairs
_fs = FileSource("/var/log/logkeys.log")
fs = FileSource("/var/log/logkeys.log")

cs = return_corrected_pairs(_fs.streamify())


# for every k characters typed show me the most incorrectly typed pairs of keys
# follow this with asking me which finger I use to type that word with

# show statistics after k keystrokes
k = 200


while True:
    print(next(cs))