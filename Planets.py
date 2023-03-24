# Importing useful functions for the program
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import linalg as la

# Used to create an easy to use gui for the program
import PySimpleGUI as gui


# Implementing Euler Solving Method
def euler_solving(x, v, t, F, m, dt):
    # Full Step ahead
    specific_force = F(x) / m
    x += dt * v
    v += dt * specific_force
    t += dt
    return x, v, t


# Implementing leapfrog solving method
def leap_frog_solving(x, v, t, F, m, dt):
    # Half Step
    x += 1 / 2 * dt * v
    t += 1 / 2 * dt

    # Update
    specific_force = F(x) / m
    v += dt * specific_force

    # Half Step
    x += 1 / 2 * dt * v
    t += 1 / 2 * dt

    return x, v, t


# General Forcing equation
def force(position, source, coefficient, power, propriety, propriety_source):
    forcing = coefficient * (position - source)
    forcing *= la.norm(position - source) ** (power - 1)
    forcing *= propriety * propriety_source
    return forcing


# Object Class
class Object:
    # Declare initial conditions
    def __init__(self, ini_pos, ini_vel, mass, interaction_space=0):
        self.positions = np.array([np.copy(ini_pos)])
        self.position = np.copy(ini_pos)
        self.pre_position = np.copy(ini_pos)
        self.velocity = np.copy(ini_vel)
        self.mass = mass
        self.interaction_space = interaction_space

        self.ini_pos = np.copy(ini_pos)
        self.ini_vel = np.copy(ini_vel)

    # Solve using euler method
    def euler_solved(self, T, F, dt):
        self.position, self.velocity, _ = euler_solving(self.position, self.velocity, T, F, self.mass, dt)
        self.positions = np.vstack([self.positions, self.position])

        return self.positions

    # Solve using leap frog
    def leap_frog_solved(self, T, F, dt):
        self.position, self.velocity, _ = leap_frog_solving(self.position, self.velocity, T, F, self.mass, dt)
        self.positions = np.vstack([self.positions, self.position])

        return self.positions

    # Reset Position
    def reset(self):
        self.position = np.copy(self.ini_pos)
        self.velocity = np.copy(self.ini_vel)
        self.positions = np.array([np.copy(self.ini_pos)])

    # Update to new position
    def update(self):
        self.pre_position = self.position

    # Generate the force this object exerts
    def generate_force(self, position, mass, mapping, interaction_space):
        if interaction_space == 0 or self.interaction_space == 0 or interaction_space != self.interaction_space:
            forcing = 0
            coefficient, power = mapping
            forcing += force(position, self.pre_position, coefficient, power, mass, self.mass)

            return forcing
        else:
            return 0


# Defines the system
class System:
    # Set the systems ininitial conditions
    def __init__(self, axis, window):
        self.objects = []
        self.dt = 0.01
        self.forcing = None
        self.axis = axis
        self.lines = []
        self.circles = []

        self.time = 0
        self.axis = axis
        self.mapping = ()
        self.window = window

    # Solve using euler method
    def euler_solved(self):
        for i, obj in enumerate(self.objects):
            def forcing(x):
                return sum([obj2.generate_force(x, obj.mass, self.mapping, obj.interaction_space)
                               for obj2 in self.objects if obj2 != obj])

            posHis = obj.euler_solved(self.time, forcing, self.dt)
            # Only keep the last 50 positions in the trace
            if len(posHis[:, 0]) > 50:
                posHis = posHis[-50:, :]

            self.lines[i].set_data(posHis[:, 0], posHis[:, 1])
            self.circles[i].set_center(tuple(posHis[-1]))

        for obj in self.objects:
            obj.update()

    # Solve using leapfrog
    def leap_frog_solved(self):
        for i, obj in enumerate(self.objects):
            def forcing(x):
                return sum([obj2.generate_force(x, obj.proprieties, self.mapping, obj.interaction_space)
                               for obj2 in self.objects if obj2 != obj])

            posHis = obj.leap_frog_solved(self.time, forcing, self.dt)
            # Only keep the last 50 positions in the trace
            if len(posHis[:, 0]) > 50:
                posHis = posHis[-50:, :]

            self.lines[i].set_data(posHis[:, 0], posHis[:, 1])
            self.circles[i].set_center(tuple(posHis[-1]))

        for obj in self.objects:
            obj.update()

    # Run the simulation
    def run_simulation(self, frame):
        event, values = self.window.read(1)

        # Close program if gui is closed
        if event == gui.WINDOW_CLOSED or values["CLOSE"]:
            import sys; sys.exit(0)

        # Reset if needed
        if event == "RESET":
            for obj in self.objects:
                obj.reset()

        # If the simulation is started
        if values["STARTSIM"]:
            # And is the first time set it up
            if not self.window["OBJECT-NUM"].Disabled:
                interaction = 1
                if values["INTERACTION"]:
                    interaction = 0

                num_of_objects = int(values["OBJECT-NUM"])
                constant = np.random.randn(2) * 100
                on_pos = values[2]
                for i in range(num_of_objects):
                    variable = np.random.randn(2) * 100
                    if values["MASS"]:
                        mass = random.randrange(1, 1000) / 10.0
                    else:
                        mass = 1
                    if on_pos:
                        variable = (variable / (np.sum(variable ** 2) ** (1 / 2)) * 1000)
                        self.objects.append(Object(np.copy(constant), np.copy(variable), mass, interaction))
                    else:
                        self.objects.append(Object(np.copy(variable), np.copy(constant), mass, interaction))

                self.objects.append(Object(np.zeros(2), np.zeros(2), values["CMASS"], 0))

                self.objects = np.array(self.objects)

                self.lines = [self.axis.plot(obj.position)[0] for obj in self.objects]
                self.circles = [plt.Circle(obj.position, self.axis.get_xlim()[1] / 70,
                                           fc=self.lines[i].get_color()) for i, obj in enumerate(self.objects)]

                for circle in self.circles:
                    self.axis.add_patch(circle)

                self.window["OBJECT-NUM"].update(disabled=True)
                self.window["INTERACTION"].update(disabled=True)
                self.window["MASS"].update(disabled=True)
                self.window["CMASS"].update(disabled=True)

                for i in range(4):
                    self.window[i].update(disabled=True)

            # Define the mapping and timestep
            self.mapping = (values["COEFFICIENT"], values["POWER"])
            self.dt = values["TIMESTEP"]

            # Run correct simulation
            if values["0"]:
                self.euler_solved()
            else:
                self.leap_frog_solved()
        return self.lines


def simulation():
    # Set up the GUI
    layout = [
        [gui.Text("Simulator")],
        [gui.HorizontalSeparator()],
        [gui.Text("Start Simulation: "), gui.Checkbox("", key="STARTSIM"), gui.Text("Close Simulation: "), gui.Checkbox("", key="CLOSE")],
        [gui.Button("Reset Simulation", enable_events=True, key="RESET")],
        [gui.Text("NumOfObjects"), gui.Slider((2, 20), 10, 1, orientation="horizontal", key="OBJECT-NUM")],
        [gui.HorizontalSeparator()],
        [gui.Text("Force Proprieties:")],
        [gui.Column([[gui.Text("Coefficient: "), gui.Slider((-1000.0, 1000.0), 10.0, orientation="horizontal", key="COEFFICIENT")]
                    ,[gui.Text("Power: "), gui.Slider((-10.0, 10.0), -2.0, orientation="horizontal", key="POWER")]], key="PROPRIETIES")],
        [gui.Text("Solving Method: "), gui.Radio("Euler Method", "SOLVER", default=True, key=0),
         gui.Radio("Leapfrog", "SOLVER", default=False, key=1)],
        [gui.Text("Simulation: "), gui.Radio("Same position, different velocities", "SIMULATION", default=True, key=2)],
        [gui.Radio("Different Position, same velocity", "SIMULATION", default=False, key=3)],
        [gui.Checkbox("Interacting particles", default=True, key="INTERACTION"),
         gui.Checkbox("Random Mass", default=True, key="MASS")],
        [gui.HorizontalSeparator()],
        [gui.Text("Timestep: "), gui.Slider((0.0, 1), 0.01, resolution=0.01, orientation="horizontal", key="TIMESTEP")],
        [gui.Text("Central Planet: ")],
        [gui.Text("Mass: "), gui.Slider((0.0, 10000.0), 10000, orientation="horizontal", key="CMASS")],
    ]

    # Set up window and plot
    window = gui.Window("Simulation", layout, resizable=True, finalize=True, size=(500, 550))
    fig, ax = plt.subplots()
    ax.set(xlim=[-1000, 1000], ylim=[-1000, 1000])

    # Create system
    system = System(ax, window)

    # Run animation with grids
    ani = animation.FuncAnimation(fig, system.run_simulation, 10, interval=0)
    plt.grid("minor")
    plt.show()

# Run program
simulation()