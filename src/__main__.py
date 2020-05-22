from stream import FileSource
from stream import return_corrected_pairs
_fs = FileSource("/var/log/logkeys.log")
fs = _fs.streamify()
cs = return_corrected_pairs(fs)

while True:
    print(next(cs))