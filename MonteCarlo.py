# Import the needed packages
import math  # To do the mathematical operations
import random  # To generate the pseudo-random numbers needed for Monte Carlo Simulations
import matplotlib.pyplot as plt  # To visualise the results


# Function to Create the figure, given points inside function,
# Outside of it, the results and the value that is being plotted
def create_fig(xi, xo, yi, yo, results, value, name):
    # The figures are saved as variables
    fig1 = plt.figure(1)
    fig2 = plt.figure(2)

    # And cleared to allow for a fresh figure to be drawn
    fig1.clf()
    fig2.clf()

    # Both figures are given axis to draw on
    ax = fig1.add_subplot(1, 1, 1)
    ax2 = fig2.add_subplot(1, 1, 1)

    # Image

    # The image is formed by plotting of points inside the function in red
    # And the points outside of it in blue
    ax.scatter(xi, yi, s=0.01, c="red")
    ax.scatter(xo, yo, s=0.01, c="blue")
    # The image is the shown
    fig1.show()

    # Accuracy graph

    # The accuracy graph is designed by plotting how the approximation given the
    # Number of points and comparing it to a fixed value which is the number we are
    # looking for
    ax2.plot(results, "k-", label=" numerical " + name)
    ax2.axhline(value, 0, len(results), color="r", linestyle="-", label=name)

    # For this graph, we want a grid, legend and axis titles to understand what is being drawn
    plt.grid(True)
    fig2.legend()
    plt.ylabel(" Result [ -] ")
    plt.xlabel(" Iteration [ -] ")

    # The image is then shown and pyplot is paused to give it time to draw the desired graph
    fig2.show()
    plt.pause(1)


# Monte Carlo simulation method
def monte_carlo_sim(N, region, cond_func, scaling_func, target, target_name):
    # Arrays for the location of points, separated by inside function
    # Or outside it
    xi = []
    yi = []
    xo = []
    yo = []

    # Array for the results
    results = []

    # Generate N points
    for i in range(N):
        # In the described region
        x = random.uniform(region[0][0], region[0][1])
        y = random.uniform(region[1][0], region[1][1])

        # Check that the point is under the curve
        cond = cond_func(x, y)
        # If it is
        if cond <= 1:
            # Add it to the inner points
            xi.append(x)
            yi.append(y)
        # Else add it to the outer points
        else:
            xo.append(x)
            yo.append(y)

        # Get the fraction of the points that are under the curve
        fraction_in = len(xi) / (i + 1)

        # Scale the fraction of areas to get the desired value and
        # Add it to the list of results
        results.append(scaling_func(fraction_in))

        # If it is 1 tenth of the way through plot the graphs
        if i % (N / 10) == 1:
            create_fig(xi, xo, yi, yo, results, target, target_name)

    # At the end print the results
    print(f"The approximation to {target_name} for {N} points is {results[-1]}")
    print(f"The actual value of {target_name} is {target}")


# Monte Carlo Pi Approximation
def monte_carlo_pi(N):
    # This uses the fact that the area of the unit circle is pi
    # Therefore the area of the quarter inside the unit square is pi/4

    # The wanted region is the one of the unit square (0,0), (0,1), (1,0), (1,1)
    region = [[0, 1], [0, 1]]

    # The condition function will be checking that the point is inside the circle
    def cond_func(x, y): return x ** 2 + y ** 2

    # And area fraction will be scaled by four to get pi
    def scaling_func(value): return 4 * value

    # Run the simulation
    monte_carlo_sim(N, region, cond_func, scaling_func, math.pi, "pi")


# Monte Carlo Approximation for ln2
def monte_carlo_ln2(N):
    # This was done independently, however clarify ability sqrt(2) was also done
    # This uses the fact that the integral of 1/x is ln(x)
    # Therefore the area going from x = 1 to x = 2 is ln2
    # The region is enclosed by a unit square, meaning that the fractional are is ln2

    # The region is as described above (1,0), (2,0), (1, 1), (2,1)
    region = [[1, 2], [0, 1]]

    # The condition is that the point is bounded by the curve y = 1/x
    # Or y * x = 1
    def cond_func(x, y): return x * y

    # The scaling function is just 1
    def scaling_func(value): return value

    # Run the simulation
    monte_carlo_sim(N, region, cond_func, scaling_func, math.log(2), "ln2")


# Monte Carlo Approximation for sqrt2
def monte_carlo_sqrt2(N):
    # This uses the fact that the integral of 1/sqrt(x) is 2 * sqrt(x)
    # Therefore the area from x = 1 to x = 2 is 2 * sqrt(2) - 2
    # In this case the region is once again a unit square

    # The region is as described before, (1,0), (2,0), (1,1), (2,1)
    region = [[1, 2], [0, 1]]

    # The condition is that the point is bounded by y = 1/sqrt(x) or
    # y * sqrt(x) = 1
    def cond_func(x, y): return math.sqrt(x) * y

    # The scaling function is simply solving for the sqrt(2) from the result of the integral
    def scaling_func(value): return (0.5 * value) + 1

    # Run the simulation
    monte_carlo_sim(N, region, cond_func, scaling_func, math.sqrt(2), "sqrt2")


# Describe the purpose of the program
print("-------Monte Carlo Approximation------")
print("\nThe purpose of this program is to run a monte carlo approximation for some values")
print("\nThis program can currently simulate: \n(1) Pi\n(2) ln(2)\n(3) sqrt(2)\n")

# Get which simulation to run
sim = -1
while not(0 < sim < 4):
    try:
        sim = int(input("What number should be approximated: "))
        if 1 > sim or sim > 3:
            raise ValueError

    except ValueError:
        print("Please enter an integer between 1 and 3")

# Get how many points should be used
N = -1
while N < 0:
    try:
        N = int(input("How many random points should be used, (for reference 10000000 may not run on a laptop): "))
        if N < 0:
            raise ValueError

    except ValueError:
        print("Please enter an integer larger the 0")

# Run the simulation
print("Beginning approximation")
match sim:
    case 1: monte_carlo_pi(N)
    case 2: monte_carlo_ln2(N)
    case 3: monte_carlo_sqrt2(N)

input()
