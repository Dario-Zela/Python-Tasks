# Importing math to observe the error in the approximation
import math


# Bisection method solver
def solve_by_bisection(fun, a, b, n):
    # Define the p value as the average point of a and b
    p = (a + b) / 2.0

    # Create the exit condition
    if n == 0:
        return p

    # Find where the zero point is
    if fun(a) * fun(p) < 0:
        # And rerun the function with the correct limits
        return solve_by_bisection(fun, a, p, n - 1)
    else:
        return solve_by_bisection(fun, p, b, n - 1)


# The solution for the original problem
def sqrt_solver():
    # Explain the program
    print("----------Square Root Solver---------")
    print("This program solves the square root of a number "
          "between 1 and 100 using the bisection method")

    # Get the value to be square rooted and check that it is valid
    num = -1
    while not (1 < num < 100):
        try:
            num = float(input("What number should be rooted: "))

        except ValueError:
            print("Please enter an rational number between 1 and 100")

    # Solve for the approximation
    val = solve_by_bisection(lambda x: num - x ** 2, 0.1, 10.1, 20)

    # Return the approximation, the real value and the error in this approximation
    print(f"The approximated value is {val} and the real value is {math.sqrt(num)}")
    print(f"The error is {val - math.sqrt(num)}, or a "
          f"percentage error of {(val - math.sqrt(num)) / math.sqrt(num) * 100}%")


# The additional task
def nth_root_solver():
    # Explain the program
    print("----------Nth Root Solver---------")
    print("This program solves the nth root of a number "
          "between 1 and 100 using the bisection method")

    # Get the value to be rooted and check that it is valid
    num = -1
    while not (1 < num < 100):
        try:
            num = float(input("\nWhat number should be rooted: "))

        except ValueError:
            print("Please enter an rational number between 1 and 100")

    # Get the power of the root and check that it is a float larger then 2
    power = -1
    while not (power >= 2):
        try:
            power = float(input("\nWhat root power should be used: "))

        except ValueError:
            print("Please enter an rational number larger then or equal to 2")

    # Solve for the approximation
    val = solve_by_bisection(lambda x: num - x ** power, 0.1, 10.1, 20)

    # Return the approximation, the real value and the error in this approximation
    print(f"\nThe approximated value is {val} and the real value is {math.pow(num, 1 / power)}")
    print(f"The error is {val - math.pow(num, 1 / power)},"
          f" or a percentage error of {abs(val - math.pow(num, 1 / power)) / math.pow(num, 1 / power) * 100}%")


nth_root_solver()
