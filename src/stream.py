from src.special import enumize, SpecialCharacters
import rx
from rx import operators as ops

def ensure_length(string, length, source):
    remaining = length - len(string)
    if remaining > 0:
        return string + source.get(remaining)
    else:
        return string

def streamify(source):
    string = source.get(10)
    processed = 0
    i = -1
    symbol = None
    last_returned = None
    while(1):
        # symbols detected previously are stored in symbol
        if symbol:
            last_returned = symbol
            yield symbol
            symbol = None
            continue
        
        i += 1
        
        try:
            char = string[i]
        except:
            processed += len(string)
            i = 0
            string = source.get(10)
            char = string[i]

        if char == '<':
            start = i
            end = None
            subsymstr = ""
            # print("char < detected")
            string = ensure_length(string, 10+start, source)

            # lookup next 10 characters:
            
            # hook to check for <#+k> entries that denotes repeat the previous entry k times
            # flag = True
            if string[start+1:start+3] == '#+':
                # print("#+ detected")
                end_bracket_at = string[start+3:].find('>')
                if end_bracket_at is not -1:
                    try:
                        repeat_times = int(string[start+3:start+3+end_bracket_at])
                        # print("This needs to be repeated: ", repeat_times)
                        # now we repeat the previously returned string that many times
                        while repeat_times > 0:
                            repeat_times -= 1
                            yield last_returned

                        end = start+3+end_bracket_at
                        i = end
                        continue
                    except:
                        # not a symbol denoting repeat entries
                        pass
            # print("starting symbol detection")
            # # this flag is false if the special symbol was a repeat k times symbol
            # if flag:
            for j,char in enumerate(string[start+1:]):
                if char == '<':
                    
                    # this means that we have consumed till end, 
                    # here as end = start, we have consumed till start
                    # which means that we revert the search
                    end = start
                    # flag = True
                    break

                elif char =='>':

                    # we have detected a less than and a greater than
                    try:
                        symbol = enumize(subsymstr)
                        # there were j characters in subsymstr
                        end = j+start+1
                    except:
                        # symbol not found error
                        # print("symbol not found error")
                        end = start

                    # anyway we break because a greater than will never be there in a special enum
                    # flag = True
                    break

                elif j == 9:
                    # flag = True
                    end = start
                    break

                else:
                    subsymstr += char
            # set current index to end
            i = end
            if symbol:
                # the symbol will be returned on top
                continue
            # otherwise the current char will be returned
            last_returned = string[i]
            # print("b",end, start, i)
            yield string[i]
            # after every yield we need to restart
            continue
        # if not <
        # print("l",i)
        last_returned = string[i]
        yield string[i]
         
class Source:
    def __init__(self, strings, join_with="<Split>"):
        self.string = join_with.join(strings)
        self.index = 0
    def get(self,count):
        slice = self.string[self.index:self.index+count]
        self.index += count
        return slice
    def streamify(self):
        return streamify(self)


# TODO reset buffer lengths?
def return_corrected_pairs(stream):
    index = -1
    previously = None
    # flag set when we are allowed to compare and send letters
    is_checking = 0
    reset = True
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
            if type(potential_corrections[0]) == type(('dummy','tuple')):
                yield potential_corrections[0]
            del(potential_corrections[0])
            continue

        if index == -1 or reset:

            index = 1
            previously = [None]
            is_checking = 0
            reset = False
            # potential_corrections = []
            while(1):
                current_element = next(stream)
                previously[0] = current_element
                if type(current_element) is not SpecialCharacters:
                    break
            # print("reset with starting element: ", previously[0])
            continue    
       

        # the index holds the position with the previous entry + 1

        current_element = next(stream)
        # print("the current element is: ", current_element)

        if current_element == SpecialCharacters.BACKSPACE:
            is_checking += 1
            index -= 1
            # print("backspace found, index reduced to: ", index)
            if(len(potential_corrections)>0):
                del(potential_corrections[-1])
            continue
        
        if type(current_element) is SpecialCharacters:
            # print("resetting.. ")
            reset = True
            continue
        
        # else: is character
        if is_checking:
            # print("yielding a corrected pair: ")

            # the current element may be later deleted in lieu of an unforeseen backspace
            # we need to wait for validation and this is slightly tricky

            # adding to potential_corrections instead
            potential_corrections.append((previously[index], current_element))
            previously[index] = current_element
            index += 1
            is_checking -= 1
            # print("replacing value at: ", index-1)
            continue
        
        # if not checking
        previously.append(current_element)
        if(len(potential_corrections)>0):
            potential_corrections.append(current_element)
        index += 1
        # print("appending value at: ", index-1)
        continue

           

def stream_consumer(stream):
    while(1):
        print(next(stream))