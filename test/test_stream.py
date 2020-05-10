import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.stream import *
from src.utils import *
from src.parse import *
from src.special import *
# from src.read import *

def test_type_fix_2():
    # this test helped fix the bug of reporting a correction when that correction was later deleted as there was a typo in the correction
    test_typo_fix_stream = return_corrected_pairs(
                            Source(
                                ['qweryt<BckSp><BckSp>tt<BckSp>y_fill_with_ten_letters']
                            ).streamify())

    try:
        assert next(test_typo_fix_stream)==('y','t')
        assert next(test_typo_fix_stream)==('t','y')
        print("Test Successful")
    except IndexError:
        print("Test Successful")
    except AssertionError:
        print("Test Failed")

def test_typo_fix_1():
    test_typo_fix_stream = return_corrected_pairs(
                            Source(
                                ['qweryt<BckSp><BckSp><BckSp>tt<BckSp>ry<BckSp><BckSp><BckSp><BckSp>eryt<BckSp><BckSp>ty_fill_with_buffer_letters']
                            ).streamify())

    # illustration of this example
    # q   w   e   r   y   t
    # q   w   e  -r- -y- -t-
    # q   w   e   t   t 
    # q   w   e   t  -t-
    # q   w   e   t   r   y
    # q   w   e   t   r   y
    # q   w  -e- -t- -r- -y-
    # q   w   e   r   y   t
    # q   w   e   r  -y- -t-
    # q   w   e   r   t   y

    # as a correction is basically, final letter in that position vs the previous letter before that final letter
    # so clearly the corrections are as follows:
    # column1: N/A
    # column2: N/A
    # column3: (e,e)
    # column4: (t,r)
    # column5: (y,t)
    # column6: (t,y)




    # column1: N/A
    # column2: N/A
    # column3: (e,e)
    # column4: (t,r)
    # column5: (y,t)
    # column6: (t,y)
    try:
        assert next(test_typo_fix_stream)==('e','e')
        assert next(test_typo_fix_stream)==('t','r')
        assert next(test_typo_fix_stream)==('y','t')
        assert next(test_typo_fix_stream)==('t','y')
        print("Test Successful")
    except IndexError:
        print("Test Successful")
    except AssertionError:
        print("Test Failed")