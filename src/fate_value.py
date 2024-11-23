"""

the affinities are: 
- Chaos (C)
- Order (O)
- Dearth (D)
- Abundance (A)

an appropriate string to generate a fate value would be something like "5CC" for 5 generic and 2 Chaos

it should always start with a number, even if there are no generic cost values

"""

import re

class FateValue:

    value_pattern = re.compile(r'(?P<generic_part>\d{0,3})(?P<affinity_part>[coda]+)|(?P<generic_whole>\d{1,3})', flags=re.IGNORECASE) #regex for a fatevalue string

    @classmethod
    def from_string(cls, value_string:str)->"FateValue":
        return_value = FateValue()

        match = re.fullmatch(FateValue.value_pattern, value_string) #verify that value_string matches the expected pattern completely
        
        if match: #if it is a match, extract data into self
            
            #keep track of the string used to generate self
            return_value.value_string = value_string 

            #evaluate the generic part of the value_string
            if generic_part:= match.group('generic_part'): #if there is a generic part of the value string...
                return_value.generic = int(generic_part) #...store it
            
            elif generic_whole:= match.group('generic_whole'): #if there isn't a generic part, see if the whole value is generic...
                return_value.generic = int(generic_whole) #...and store it if it is
                
            else: #...if neither of those cases are true, there is no generic part
                return_value.generic = 0 #...so the generic value is 0

            #evaluate the non-generic part
            if affinity_part := match.group('affinity_part'):
                affinity_part = str.upper(affinity_part) #convert to upper case
                return_value.chaos = str.count(affinity_part,'C') #count all C in the cost; each is another chaos
                return_value.order = str.count(affinity_part,'O') #count all O in the cost; each is another order
                return_value.dearth = str.count(affinity_part,'D') #count all D in the cost; each is another dearth
                return_value.abundance = str.count(affinity_part,'A') #count all A in the cost; each is another abundance

            return return_value
        else:
            print(f"FateValue parse failed on string {value_string}")
            print(r"Format should match the pattern \d{0,3}[coda]*|\d{1,3} ")
            print(r"\te.g.: \'5CC\' or \'5cc\' for 5 generic and 2 Chaos; \'5\' for 5 generic and nothing else; \'DD\'  or \'dd\' for 2 dearth")
            return None
        

        
    def __init__(self, generic:int=0, chaos:int=0, order:int=0, dearth:int=0,abundance:int=0):
        
        #since this constructor doesn't provide a value_string like the above one, it will have to be generated
        self.value_string:str = ''

        if generic:
            self.value_string += str(generic)

        if chaos:
            self.value_string += (str('c') * chaos)

        if order:
            self.value_string += (str('o') * order)

        if dearth:
            self.value_string += (str('d') * dearth)

        if abundance:
            self.value_string += (str('a') * abundance)

        self.generic:int = generic
        self.chaos:int = chaos
        self.order:int = order
        self.dearth:int = dearth
        self.abundance:int = abundance

    def get_converted_cost(self) -> int:
        print(self)
        return (
                self.generic + 
                self.chaos + 
                self.order +
                self.dearth +
                self.abundance
            )
        
    @classmethod
    def copy(cls, other: "FateValue") -> "FateValue":
        '''
        returns a deep copy of the other FateValue
        '''
        return FateValue(
            other.generic,
            other.chaos,
            other.order,
            other.dearth,
            other.abundance
        )

    def __str__(self):
        return str(self.value_string)
    
    def __eq__(self, other: "FateValue") -> bool:
        return (
            self.value_string == other.value_string
            and self.generic == other.generic
            and self.chaos == other.chaos
            and self.order == other.order
            and self.dearth == other.dearth
            and self.abundance == other.abundance
            and self.get_converted_cost() == other.get_converted_cost()
        )
    
    def add(self, other: "FateValue") -> "FateValue":
        return(
            FateValue(
                self.generic + other.generic,
                self.chaos + other.chaos,
                self.order + other.order,
                self.dearth + other.dearth,
                self.abundance + other.abundance
            )
        )
    
    def generic_difference(self, other: "FateValue") -> int:
        return self.generic - other.generic if self.generic > other.generic else 0
        
    def chaos_difference(self, other: "FateValue") -> int:
        return self.chaos - other.chaos if self.chaos > other.chaos else 0
        
    def order_difference(self, other: "FateValue") -> int:
        return self.order - other.order if self.order > other.order else 0
    
    def dearth_difference(self, other:"FateValue") -> int:
        return self.dearth - other.dearth if self.dearth > other.dearth else 0
    
    def abundance_difference(self, other:"FateValue") -> int:
        return self.abundance - other.abundance if self.abundance > other.abundance else 0
    
    def reduce_by(self, other:"FateValue", min:int = 0) -> "FateValue":
        """
        reduces the FateValue by the passed amount, clamped at the min value.

        min should never be negative

        does not take into account whether the current FaceValue has the necessary values from the passed FateValue

        WARNING: be aware it is possible to actually increase values under the wrong circumstances,
        specifically: if min is higher than the current value of an aspect
        """

        return FateValue(
            self.generic - other.generic if self.generic - other.generic > min else min,
            self.chaos - other.chaos if self.chaos - other.chaos > min else min,
            self.order - other.order if self.order - other.order > min else min,
            self.dearth - other.dearth if self.dearth - other.dearth > min else min,
            self.abundance - other.abundance if self.abundance - other.abundance > min else min
        )
    
    def spend(self, other:"FateValue") -> "FateValue":
        """
        checks if the currentFateValue can 'afford' to spend the passed fate value.

        For example: 5cc would be able to 'spend' 2c and be left with 3c.
        
        5cc would *not* be able to 'spend' 2o - because it doesn't have any o.

        if it's able to spend, it returns the difference as a FateValue.

        if it isn't able to spend, it returns Nothing.
        """
        #TODO checks if the current FateValue can 'afford' to spend the passed fate value
        # returns a copy of a FateValue that is the difference between the two FateValues if possible
        # if not possible, returns None



        pass

    def __repr__(self):
        return f'FateValue: {self.value_string} \t generic:{self.generic}, chaos:{self.chaos}, order:{self.order}, dearth:{self.dearth}, dearth:{self.abundance}, converted:{self.get_converted_cost()}'