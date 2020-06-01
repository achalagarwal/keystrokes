from stream import FileSource, return_corrected_pairs_with_counter
import time, subprocess
from functools import reduce

_fs = FileSource("/var/log/logkeys.log")
cs_with_counter = return_corrected_pairs_with_counter(_fs.streamify())

# for every k characters typed show me the most incorrectly typed pairs of keys
# follow this with asking me which finger I use to type that word with

# show statistics after k keystrokes
# but not if a long time has passed between those k keystrokes
k = 20
gap_in_seconds = 900

prev_count = 0
prev_time = time.time()
# store corrections with frequency
corrections = dict()

while True:

    correction, counter = next(cs_with_counter)

    if correction[0] is not correction[1]:
        corrections[correction] = corrections.get(correction, 0) + 1

    if counter - prev_count > k:

        # check if time gap is too long
        if time.time() - prev_time > gap_in_seconds:

            # just reset and continue
            prev_count = counter
            prev_time = time.time()
            corrections = dict()
            continue

        # compute statistics
        
        ## get mistyped percentage
        total_keys_typed = counter - prev_count
        total_effective_typos = reduce(lambda x,y: x+y, corrections.values(),0)

        ### multiplying by 2 to get the truer error percentage 
        ### as for each key that was typed in error, there are effectively two keys that are error related
        percentage_error = total_effective_typos*100.0*2/total_keys_typed

        ## get top 3 most frequently mistyped
        sorted_corrections = sorted(corrections.items(), key=lambda x: x[1], reverse=True)

        first = sorted_corrections[0] if len(sorted_corrections)>0 else (('', ''),'')
        second = sorted_corrections[1] if len(sorted_corrections)>1 else None
        third = sorted_corrections[2] if len(sorted_corrections)>2 else None
        
        heading = "{error:.2f}% error!".format(error = percentage_error)
        description = "The top worst types are: \n{first}{second}{third}".format(
            first = first[0][0] + " --> " + first[0][1] +'\n',
            second = second[0][0] + " --> " + second[0][1] + '\n' if second else '',
            third = third[0][0] + " --> " + third[0][1] if third else '')

        # show statistics

        proc = subprocess.Popen(["dbus-send", "--dest=com.keystrokes.notifs", "--print-reply", "--type=method_call", "/com/keystrokes/notif/show","com.keystrokes.notif.show","string:"+heading, "string:"+description, "string:na"])
     
        # reset
        prev_count = counter
        prev_time = time.time()
        corrections = dict()
        

