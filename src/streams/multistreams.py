import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stream import FileSourceExisting
from special import SpecialCharacters
from utils import is_word_separator, finger_distance
# return corrected pairs
# but counts all non special keystrokes

# so before yielding check the sync value,
# after yielding, receive the next sync value
# but if the sync value is more, yield None 

def return_corrected_pairs_with_counter(stream, syncee=True, syncer=False):
    index = -1
    previously = None
    counter = 0
    # flag set when we are allowed to compare and send letters
    is_checking = 0
    reset = True
    sync_on = yield

    # this stores the detected corrections
    # they are potential because we might correct a correction thus nullifying the previous correction

    # this could also be (better) thought of as an N-back recorder
    potential_corrections = []
    # this is the safety buffer after which we can assume that there will be no more corrections on corrections
    # this safety buffer will apply on is_checking, so safety_buffer letters after is_checking becomes false
    safety_buffer = 10
    # need to initialise with at least one character to prevent errors by one
    while(1):
         
        if len(potential_corrections) >= safety_buffer:
            # the potential corrections store tuple if its a correction or the character if its just a letter history
            if type(potential_corrections[0][1]) == type(('dummy','tuple')):
                if potential_corrections[0][1][1] <= sync_on:
                    sync_on = yield (potential_corrections[0], counter)
                    del(potential_corrections[0])
                else:
                    sync_on = yield None
                # sync_on = yield
            else:
                # delete the non error
                del(potential_corrections[0])
            continue
        
        # TODO
        # the reset is quite questionable and should be relaxed

        # TODO
        # Now there are multiple copies of the same code and that's annoying, fixit!
        if index == -1 or reset:

            index = 1
            previously = [None]
            is_checking = 0
            reset = False
            # potential_corrections = []
            while(1):
                current_element_w_count = next(stream)
                
                previously[0] = current_element_w_count
                if type(current_element_w_count[0]) is not SpecialCharacters:
                    break
            # print("reset with starting element: ", previously[0])
            continue    
       

        # the index holds the position with the previous entry + 1
        else:
            current_element_w_count = next(stream)

        if type(current_element_w_count[0]) is not SpecialCharacters:
            counter += 1
        # print("the current element is: ", current_element)

        if current_element_w_count[0] == SpecialCharacters.BACKSPACE:
            is_checking += 1
            index -= 1
            # print("backspace found, index reduced to: ", index)
            if(len(potential_corrections)>0):
                del(potential_corrections[-1])
            continue
        
        if type(current_element_w_count[0]) is SpecialCharacters:
            # print("resetting.. ")
            reset = True
            continue
        
        # else: is character
        if is_checking:
            # print("yielding a corrected pair: ")

            # the current element may be later deleted in lieu of an unforeseen backspace
            # we need to wait for validation and this is slightly tricky

            # adding to potential_corrections instead
            potential_corrections.append((previously[index], current_element_w_count))
            previously[index] = current_element_w_count
            index += 1
            is_checking -= 1
            # print("replacing value at: ", index-1)
            continue
        
        # if not checking
        previously.append(current_element_w_count)
        if(len(potential_corrections)>0):
            potential_corrections.append(current_element_w_count)
        index += 1
        # print("appending value at: ", index-1)
        continue

def return_corrected_pairs(stream, syncee=True, syncer=False):
    index = -1
    previously = None
    counter = 0
    # flag set when we are allowed to compare and send letters
    is_checking = 0
    reset = True
    sync_on = yield

    # this stores the detected corrections
    # they are potential because we might correct a correction thus nullifying the previous correction

    # this could also be (better) thought of as an N-back recorder
    potential_corrections = []
    # this is the safety buffer after which we can assume that there will be no more corrections on corrections
    # this safety buffer will apply on is_checking, so safety_buffer letters after is_checking becomes false
    safety_buffer = 10
    # need to initialise with at least one character to prevent errors by one
    while(1):
         
        if len(potential_corrections) >= safety_buffer:
            # the potential corrections store tuple if its a correction or the character if its just a letter history
            if type(potential_corrections[0][1]) == type(('dummy','tuple')):
                if potential_corrections[0][1][1] <= sync_on:
                    sync_on = yield potential_corrections[0][0][0], potential_corrections[0][1][0]
                    del(potential_corrections[0])
                else:
                    sync_on = yield None
                # sync_on = yield
            else:
                # delete the non error
                del(potential_corrections[0])
            continue
        
        # TODO
        # the reset is quite questionable and should be relaxed

        # TODO
        # Now there are multiple copies of the same code and that's annoying, fixit!
        if index == -1 or reset:

            index = 1
            previously = [None]
            is_checking = 0
            reset = False
            # potential_corrections = []
            while(1):
                current_element_w_count = next(stream)
                
                previously[0] = current_element_w_count
                if type(current_element_w_count[0]) is not SpecialCharacters:
                    break
            # print("reset with starting element: ", previously[0])
            continue    
       

        # the index holds the position with the previous entry + 1
        else:
            current_element_w_count = next(stream)

        if type(current_element_w_count[0]) is not SpecialCharacters:
            counter += 1
        # print("the current element is: ", current_element)

        if current_element_w_count[0] == SpecialCharacters.BACKSPACE:
            is_checking += 1
            index -= 1
            # print("backspace found, index reduced to: ", index)
            if(len(potential_corrections)>0):
                del(potential_corrections[-1])
            continue
        
        if type(current_element_w_count[0]) is SpecialCharacters:
            # print("resetting.. ")
            reset = True
            continue
        
        # else: is character
        if is_checking:
            # print("yielding a corrected pair: ")

            # the current element may be later deleted in lieu of an unforeseen backspace
            # we need to wait for validation and this is slightly tricky

            # adding to potential_corrections instead
            potential_corrections.append((previously[index], current_element_w_count))
            previously[index] = current_element_w_count
            index += 1
            is_checking -= 1
            # print("replacing value at: ", index-1)
            continue
        
        # if not checking
        previously.append(current_element_w_count)
        if(len(potential_corrections)>0):
            potential_corrections.append(current_element_w_count)
        index += 1
        # print("appending value at: ", index-1)
        continue


# sends the sync clock
def word_context_stream(stream, safety_buffer=10, sync_clock=True):
    index = 0 
    buffer = [None for _ in range(2*safety_buffer)]
    current_word = ''
    sync_clock = 0
    while(1): 

        # check buffer and generate word contexts
        if index == 2*safety_buffer:
            
            _index = 0
            while(_index < safety_buffer):
                
                symbol_w_counter = buffer[_index]
                buffer[_index] = buffer[_index + safety_buffer]
                _index += 1

                if is_word_separator(symbol_w_counter[0]):
                    yield (current_word, sync_clock)
                    current_word = ''
                
                elif type(symbol_w_counter[0]) is not SpecialCharacters:
                    current_word += symbol_w_counter[0]
                    sync_clock = symbol_w_counter[1]
                
                elif symbol_w_counter[0] == SpecialCharacters.BACKSPACE:
                    current_word = current_word[0:-1]
                    sync_clock = symbol_w_counter[1]

            index = safety_buffer
            continue
        
        symbol_w_counter = next(stream)

        # backspaces need to be handled separately
        # they have to be handled here before the characters are stored in the buffer
        # this way the capture above can be direct
        # TODO
        # so this portion of the code could be another stream
        # and this stream can be then always used for the subsequent connection streams

        # if backspace
        # update syncclock
        # and negative update the index
        
        if symbol_w_counter[0] == SpecialCharacters.BACKSPACE:
            if index > 0:
                index -=1 
                buffer[index]
                if index > 0:
                    buffer[index-1] = (buffer[index-1][0],symbol_w_counter[1])
                # how can we update the sync_value on a backspace
                # do I need to keep track of backspace sync?
            continue
        buffer[index] = symbol_w_counter
        index += 1
        continue



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

    pdb.set_trace()
    stream_syncer = word_context_stream(FileSourceExisting(filename).streamify(counter=True))
    # current_word, sync_value = next(stream_syncer)

    stream_syncee = return_corrected_pairs(FileSourceExisting(filename).streamify(counter=True))
    
    # initialise syncee
    stream_syncee.send(None)

    # take from syncer
    # send to syncee
    # take from syncee while None
    pdb.set_trace()
    while(1):
        current_word, sync_value = next(stream_syncer)
        # print(current_word)
        # typos = 
        recv = stream_syncee.send(sync_value)
        errors = []
        while recv is not None:
            errors.append(recv)            
            recv = stream_syncee.send(sync_value)

        if len(errors)>0:

            # print(current_word)
            # print(errors)
            # analytics:

            # correction distance for each errors
            distances = []

            # letter belongs in the new word?
            belongs = []

            # adjacent corrections
            adjacent = []

            # cascading corrections
            cascading = []

            print(current_word)

            for i,error in enumerate(errors):
                distances.append(finger_distance(error[0], error[1]))
                belongs.append(error[1] in current_word)
                # mis-ordering of characters, this typically happens with the characters that
                # are adjacent
            
                

                if i < len(errors)-1:
                    if errors[i][0] == errors[i+1][1] and errors[i][1] == errors[i+1][0]:
                        adjacent.append(True)
                        adjacent.append(True)
                    else:
                        adjacent.append(None)
                else:
                    if not len(adjacent) == len(errors):
                        adjacent.append(None)

                cascading_flag = True

                if i > 0:
                    # the previous correction can be checked for a cascading loss
                    # here i can check the cascading loss
                    # here check the previous index
                    # need the global counter of the error to check if the errors are indeed adjacent
                    # this can be re-enabled from the stream but then the other statistic measures need to be fixed]
                    
                    if errors[i-1][0] == errors[i][1]:
                        cascading.append(True)
                        cascading_flag = False

                         
                if i < len(errors)-1:
                    
                    if errors[i][0] == errors[i+1][1] and cascading_flag:
                        cascading.append(True)
                        cascading_flag = False

                if cascading_flag:

                    cascading.append(False)
                    cascading_flag = False

                    # trying to solve the issue with the 
                    # cascading errors
                    # the cascading errors come from a single source of error
                    # which leads to multiple errors
                    # eg:
                    # acchal
                    # four backspaces are required
                    # the the correction for just the extra c
                    # is 4

                
                
            print(errors)
            print(distances)
            print(belongs)
            print(adjacent)
            print(cascading)

            # 
            # if the new letter is in the word that means that it was a correction
            # metric how close the correction was
            print('--------')

    # stream_1 will return the counter on which it stopped
    # stream_2 will return 
    
import pdb
if __name__ == '__main__':
    # pdb.run('return_corrected_pairs_with_word_context("/var/log/logkeys.logsss")')
    # return_corrected_pairs_with_word_context("../data/manual2.log")
    return_corrected_pairs_with_word_context("../data/keylogs.log")