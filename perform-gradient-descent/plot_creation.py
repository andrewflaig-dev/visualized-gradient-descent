import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import cm
import sympy as sp

# Core data for every graph to be made
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

def create_surface(x, y, z):
    ax.plot_surface(x, y, z,
                        cmap=cm.plasma,
                        linewidth=0,
                        alpha=0.75,
                        antialiased=True)

def paraboloid():
    def z_func(x, y):
        return x**2 + y**2
    Z = z_func(X, Y)

    create_surface(X, Y, Z)

    ax.set_title("Paraboloid Curve")
    ax.view_init(elev=35)

    return (fig, ax, z_func)

def ripple():
    def z_func(x, y):
        r = sp.sqrt(x**2 + y**2)
        return sp.sin(r) / (r + 1e-5)

    Z = z_func(X, Y)

    create_surface(X, Y, Z)

    ax.set_title("Ripple Surface")
    ax.view_init(elev=25)

    return (fig, ax, z_func)
