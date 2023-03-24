# This project attempts to be a simple linear simultaneous equations solver with complex coefficients
# This is done using matrix inversion through the numpy library

# The numpy library is imported
import numpy

# The use of the program is explained to the user
print("----Welcome to the Simultaneous Equation Solver----")
print("\nThis program is designed to solve equations of the type:")
print("A1x+B1y+C1z+... = Z1")
print("A2x+B2y+C2z+... = Z2")
print("ect\n")

# The user is prompted to enter the number of unknowns that the program will be solving for
# The size of the matrix is taken as input and checked to be an integer larger then 2
matSize = 0
while matSize == 0:
    try:
        matSize = int(input("Please enter the number of unknowns: "))
        if matSize < 2:
            matSize = 0
            raise ValueError()
    except ValueError:
        print("\nThe coefficient must be a integer larger then 2")

# The user is warned of the solver's limitations
print("\nWarning, this solver will only allow for the number of simultaneous equations to be the number of unknowns\n")

# The matrix containing the coefficients of the simultaneous equations
MatrixOfCoefficients = []
# The vector containing the result of each equation
VectorOfResults = []

# Iterating through all items
for i in range(matSize):
    CurrentSet = []
    for j in range(matSize):

        # The coefficient is taken as input and checked to be complex
        coefficient = 0
        while coefficient == 0:
            try:
                coefficient = complex(
                    input(f"Please enter to coefficient for the {j + 1} unknown in the {i + 1} equation: "))
            except ValueError:
                print("\nThe coefficient must be a complex number")

        # And then added to the list of coefficients for this equation
        CurrentSet.append(coefficient)

    # The result of this equation is taken and checked to be complex
    result = 0
    while result == 0:
        try:
            result = complex(
                input(f"\nPlease enter to result to equation {i + 1}: "))
        except ValueError:
            print("\nThe coefficient must be a complex number")

    print("")

    # The values are then added to the respective lists
    VectorOfResults.append(result)
    MatrixOfCoefficients.append(CurrentSet)

# The lists are then converted into matrix objects
MatrixOfCoefficients = numpy.matrix(MatrixOfCoefficients)
VectorOfResults = numpy.matrix(VectorOfResults).transpose()

# If the coefficient of the matrix is zero there is no unique solution
# Therefore the program terminates
if numpy.linalg.det(MatrixOfCoefficients) == 0:
    print("The equation you submitted does not have a unique solution")
    import sys; sys.exit(0)

# Else the unknowns are calculated via matrix multiplication
VectorOfUnknowns = numpy.linalg.inv(MatrixOfCoefficients) * VectorOfResults

# Floating point digits give unnecessarily long expansions for hard to write numbers:
# Such as 13 = 12.99999999, therefore to get a better output, the text from the string version
# Of the matrix is extracted and printed out
pos = 1
result = f"\nThe unknowns are: \n{pos} = "
number = str(VectorOfUnknowns)

# For all characters in the text of the string
for i in range(len(number)):
    # Check for any numeric character or an imaginary unit
    if number[i].isnumeric() or number[i] == "j":
        result += number[i]

    # Check if there is a non-trivial dot
    elif number[i] == "." and number[i + 1].isnumeric():
        result += number[i]

    # Convert the closing bracket with the start of a new unknown
    elif number[i] == "]":
        pos += 1
        result += f"\n{pos} = "

    # Check for the presence of sign digits
    elif number[i] == "+" or number[i] == "-":
        result += " " + number[i] + " "

# Print everything except for the last 9 characters as there will be 2 more
# closing brackets than there will be unknowns
print(result[:-9])
