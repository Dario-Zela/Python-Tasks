# Importing RE to find sequence terms
from re import finditer

# Import literal eval for safe string execution
from ast import literal_eval

# All functions in math and cmath are imported to allow for easy access to math functions
# in the sequence expansion
from math import *
from cmath import *


# The original task
def golden_ratio():
    print("-----Golden Ratio-------")
    print("This program will generate the intermediate solutions for the following sequence")
    print("1+1/(1+...)\n\n")

    a = 1
    for i in range(20):
        print(a)
        a = 1 + 1 / a


# Checks if the input is the correct format
def sanitised_input(cast, input_text, error_text, test=lambda var: False):
    variable = None
    while variable is None:
        try:
            # Check that the variable is the correct type
            variable = cast(
                input(input_text))

            # Apply extra conditions
            if test(variable):
                variable = None
                raise ValueError

            # If error occurs send the error message and try again
        except ValueError:
            print(error_text)

    # Return requested variable
    return variable


# Helper class to have a set of terms that quickly switch from
# Previous term to next term
class cyclic_list:
    def __init__(self, data):
        # Some constants for the list are set up
        self.max_size = len(data)
        self.data = data
        self.size = 0
        self.start = 0

    # The get item method is instantiated
    def __getitem__(self, i):
        if i >= self.max_size:
            raise IndexError

        return self.data[(self.start + i) % self.max_size]

    # The method to add the next term to the set of terms used in the sequence
    def next(self, data):
        self.data[self.start] = data
        self.start = (self.start + 1) % self.max_size


def sequence_solver():
    # Some explanation of the program's purpose
    print("-----Sequence Solver-----\n")
    print("This program will generate the next n terms of a generator function\n")
    print("The format of the generator function accepted by the program is:")
    print("aN = f(a1, a2 ...)")
    print("Where a1 is the nth term in the sequence, a2 is the n + 1 term and so on")
    print("N is the index term that is generated")

    print("\nAn example for the golden ration sequence would be")
    print("1 + 1/a1\n")

    # Warn the user of the eval method being used
    print("The program uses a dangerous function to generate the sequence")
    print("You may use the safe mode, but will be restricted in running only basic maths \n"
          "operations and and complex numbers may not function properly")
    print("Otherwise you may use unsafe mode and allow for full functionality but \n"
          "must beware of what is typed as it may cause permanent damage to your computer \n"
          "if the generator function contains non-maths python methods")
    safe = sanitised_input(str, "Do you wish to use safe mode: ", "Please enter a boolean (True or False)",
                           lambda i: i == "True" or i == "False")

    # Convert from string to boolean
    if safe == "True":
        safe = True
    else:
        safe = False

    # The number of results is taken
    num_of_terms = sanitised_input(int, "Please enter the number of terms you wish to print out: "
                                   , "Please enter an integer larger the 1"
                                   , lambda i: i < 1)

    # The number of terms used in the generator funation is taken
    num_of_initial_terms = sanitised_input(int, "Please enter the number of terms the generator function requires: "
                                           , "Please enter an integer larger the 1 but less then 10"
                                           , lambda i: (1 > i > 10))

    # The initial terms are collected and added to a cyclic list
    initial_terms = []
    for i in range(num_of_initial_terms):
        initial_terms.append(sanitised_input(complex, "Please enter the " + str(i) + "th initial term: ",
                                             "Please enter a complex number"))
    terms = cyclic_list(initial_terms)

    # The generator function is taken
    generator_function = input("Please enter the generator function:\n")

    for i in range(num_of_terms):
        k = None
        function = ""
        start = 0

        # The terms in the form an are switched with their numerical counterparts
        for j in finditer("a\d", generator_function):

            k = int(generator_function[j.start() + 1]) - 1

            # If the value of n is larger the maximum value, the function is invalid
            if k >= num_of_initial_terms:
                print("The generator function was not valid")
                return

            function += generator_function[start:j.start()] + str(terms[k])
            start = j.start() + 2

        if k is not None:
            function += generator_function[start:]

        if len(function) == 0:
            function = generator_function

        # If the code is in safe mode, use literal eval
        if(safe):
            try:
                # The generator function is executed
                term = literal_eval(function)
            except:
                print("The generator function was not valid")
                return
        # Else use regular eval
        else:
            try:
                # The generator function is executed
                term = eval(function)
            except:
                print("The generator function was not valid")
                return

        # The next term is added to the list and printed
        terms.next(term)
        print(term)


if __name__ == "__main__":
    sequence_solver()
