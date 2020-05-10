from enum import Enum

class SpecialCharacters(Enum):
    BACKSPACE = 1
    CTRL = 2
    SHIFT = 3
    OS = 4
    ALT = 5
    ARROW = 6
    ENTER = 7
    DELETE = 8
    IGNORE = 9
    REPEAT = 10
    FUNC = 11
    KEYPAD = 12
    ESC = 13
    INS = 14
    MENU = 15
    PGUP = 16
    TAB = 17
    META = 18

def enumize(string):
    d = {
        'AltGr': SpecialCharacters.ALT,
        'BckSp': SpecialCharacters.BACKSPACE,
        'CpsLk': SpecialCharacters.IGNORE,
        'Del': SpecialCharacters.DELETE,
        'Down': SpecialCharacters.ARROW,
        'Enter': SpecialCharacters.ENTER,
        'Esc': SpecialCharacters.ESC,
        'F12': SpecialCharacters.FUNC,
        'F4': SpecialCharacters.FUNC,
        'Ins': SpecialCharacters.INS,
        'KP0': SpecialCharacters.KEYPAD,
        'KP1': SpecialCharacters.KEYPAD,
        'KP2': SpecialCharacters.KEYPAD,
        'KP3': SpecialCharacters.KEYPAD,
        'KP4': SpecialCharacters.KEYPAD,
        'KP5': SpecialCharacters.KEYPAD,
        'KP6': SpecialCharacters.KEYPAD,
        'KP7': SpecialCharacters.KEYPAD,
        'KP8': SpecialCharacters.KEYPAD,
        'KP9': SpecialCharacters.KEYPAD,
        'KPEnt': SpecialCharacters.KEYPAD,
        'LAlt': SpecialCharacters.ALT,
        'RAlt': SpecialCharacters.ALT,
        'LCtrl': SpecialCharacters.CTRL,
        'LMeta': SpecialCharacters.OS,
        'RMeta': SpecialCharacters.OS,
        'LShft': SpecialCharacters.SHIFT,
        'Left': SpecialCharacters.ARROW,
        'Menu': SpecialCharacters.MENU,
        'NumLk': SpecialCharacters.IGNORE,
        'PgUp': SpecialCharacters.PGUP,
        'RCtrl': SpecialCharacters.CTRL,
        'RShft': SpecialCharacters.SHIFT,
        'Right': SpecialCharacters.ARROW,
        'Tab': SpecialCharacters.TAB,
        'Up': SpecialCharacters.ARROW,
        'Split': SpecialCharacters.META
    }
    return d[string]