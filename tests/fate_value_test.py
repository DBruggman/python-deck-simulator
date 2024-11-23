import unittest
from src.fate_value import FateValue



class TestFateValue(unittest.TestCase):


    #test to make sure that a properly called instantiation of FateValue.from_string will work
    def test_from_string_good_input(self):
        print('testing FateValue.from_string with good inputs')
        
        good_inputs = {
            '5cc' : FateValue(generic=5,chaos=2),
            'aa'  : FateValue(abundance=2),
            '10'  : FateValue(generic=10),
            'ccooddaa' : FateValue(chaos=2,order=2,dearth=2,abundance=2),
            '0' : FateValue()
        }

        for s,v in good_inputs.items:
            curr = FateValue.from_string(s)
            self.assertTrue(curr == v)

    #TODO: come up with a test that makes sure bad input will cause .from_string to return None
    def test_from_string_bad_input(self):
        bad_input = FateValue.from_string('your mother')
        self.assertIsNone(bad_input)

    #TODO: create a test that verifies multiple different types or styles of input, both valid and invalid.
    # for example, all of the following are valid: 1c co 5 65 959 coda 0
    # and all of the following should be invalid: c1 oc 1coda2 1234 1234coda coco adoc c1oda
    # the regex should pick out most of these - but there isn't really anything programmed as of yet that verifies the characters are in the right order
    # so is it possible the two equivalent values 1cca and 1cac would be evaluated differently or at least have different strings or have some odd artifact of some sort?

    #TODO: come up with a test that handles over-addition
    #  if the generic value is 4 or more digits after two valid FateValues are added together, what should happen? 
    #  is there an upper limit of what the generic value can be? (something that costs 9999 is impossible to play, right?)

if __name__ == '__main__':
    unittest.main()

