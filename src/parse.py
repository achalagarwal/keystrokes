from datetime import datetime
from time import strptime
from enum import Enum
import re

def process_raw_line(raw_line):
    date_text = raw_line.split(" > ")
    
    try:
        # if date_text[0]
        if (date_text[0].find("Logging stopped")) > -1 or  (date_text[0].find("Logging started")) > -1:
            return None
        if date_text[0] == '' and len(date_text) == 1:
            return None
        assert(len(date_text)==2)
        date = date_text[0]
        text = date_text[1]
        return (strptime(date, "%Y-%m-%d %H:%M:%S-0700"), text)
    except Exception as e:
        print(date_text + " has a parsing error: len != 2 " + str(e))
    # print(raw_line.split(" > "))


def parse(file_name, offset=70):
    _file = open(file_name,"r") 
    raw_string = _file.read()
    raw_lines = raw_string.split('\n')
    clean_lines = []
    for raw_line in raw_lines:
        # print(raw_line)
        line = process_raw_line(raw_line)
        if line:
            clean_lines.append(line)
    clean_lines = clean_lines[offset:]

