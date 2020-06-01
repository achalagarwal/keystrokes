from stream import FileSource
from stream import return_corrected_pairs_with_counter
_fs = FileSource("/var/log/logkeys.log")
fs = FileSource("/var/log/logkeys.log")
import time
from functools import reduce
import subprocess,os
my_env = os.environ

# cs = return_corrected_pairs(_fs.streamify())
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

    # print("debug-->", correction, counter)
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
        description = "The top 3 worst types are: \n{first}\n{second}\n{third}".format(
            first = first[0][0] + " --> " + first[0][1],
            second = second[0][0] + " --> " + second[0][1] if second else None,
            third = third[0][0] + " --> " + third[0][1] if third else None)

        # show statistics

        proc = subprocess.check_output(["dbus-send", "--dest=com.keystrokes.notifs", "--print-reply", "--type=method_call", "/com/keystrokes/notif/show","com.keystrokes.notif.show","string:"+heading, "string:"+description, "string:na"])
        # ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("The exit code was: %d" % list_files.returncode)
        # stdout, stderr = proc.communicate()
        # print(stdout)
        # print(stderr)
        print(proc)
        # reset
        prev_count = counter
        prev_time = time.time()
        corrections = dict()
        

    


    # print(next(cs))