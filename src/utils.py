
from special import SpecialCharacters
# finger with letters maps fingers to the letters that they should be typing
# obviously this could change from person to person
# but the default is the most standard one

finger_with_letters = {
    0:{'q','a','z'}, 
    1:{'w','s','x'}, 
    2:{'e','d','c'}, 
    3:{'r','f','v', 't', 'g','b'}, 
    4:{'u','j','m', 'y','h','n'}, 
    5:{'i','k',','}, 
    6:{'o','l','.'}, 
    7:{'p',';','/'},
    }

letter_to_finger = dict()
for k, v in finger_with_letters.items():
    for letter in v:
        letter_to_finger[letter] = k

def finger_distance(l1, l2):
    try:
        return abs(letter_to_finger[l1] - letter_to_finger[l2])
    except:
        return -1

def is_word_separator(symbol):
    
    # switcher for special characters
    specialChars = {
        'default': True,
        SpecialCharacters.SHIFT: False,
        SpecialCharacters.KEYPAD: False,
    }

    # switcher for normal chars
    normalChars = {
        'default': False,
        ' ': True,
        ',': True, 
        '.': True, 
        '_': True, 
        '{': True, 
        '}': True, 
        '(': True, 
        ')': True, 
        ';': True,
        '/': True,
        '\\': True
    }

    if symbol is SpecialCharacters:
        return specialChars.get(symbol, specialChars.get('default'))

    # elif symbol is None:
    #     return False

    else:
        return normalChars.get(symbol, normalChars.get('default'))
