from stream import word_context_stream,
                   return_corrected_pairs_with_word_context,
                   FileSource


# TODO: Create a word context aware character stream
# Easy to do: send a tuple (char, word_context)
# word context breaks/changes when there are spaces? but what about a backspace? 
# a little complicated given that we might have to chain things

# TODO: There are two ways to do this
# we can have a word stream, a correction stream and connect them both
# this one is tough but the implementation will be so much cleaner

# return corrected pairs
# but counts all non special keystrokes
def return_corrected_pairs_with_word_context(filename):

    # the common stream should have a counter 
    # so that it could be synchronised

    stream_1 = word_context_stream(FileSource(filename, counter=True))
    stream_2 = return_corrected_pairs_with_word_context(FileSource(filename, counter=True))

