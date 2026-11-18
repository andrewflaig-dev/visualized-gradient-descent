import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

## Helper Functions
def randrange(n, vmin, vmax):
    '''
    This is to ensure that the data will fit within the constraints of the plot
    '''
    return (vmax - vmin) * np.random.rand(n) + vmin

def create_gif(fig, ax, file_name, elevation=20, degree = 3, fps=20):
    '''
    Creates a gif that does a 360 around the 3D graph
    Goal: Learning animation of 3D Graphs
    '''
    anim = FuncAnimation(fig, lambda a: ax.view_init(elev=elevation, azim=a),
                        frames=range(0, 360, degree))
    anim.save(f"images/{file_name}.gif", writer=PillowWriter(fps=fps))

    plt.close(fig) # Save Memory

def surface_function(X, Y):
    # For practice, I'm going to make a ripple cause it looks cool [Z = sin(sqrt(X^2 + Y^2)) / sqrt(X^2 + Y^2))]
    R = np.sqrt(X**2 + Y**2)
    return np.sin(R) / (R + 1e-5) # 1e-5 is to avoid dividing by zero

## Graph Creation 
# Create 3D Parametric (line) plot
def create_3d_line():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    theta = np.linspace(0, 10, 100)
    
    x = np.sin(theta)
    y = np.cos(theta)
    z = theta

    ax.plot(x,y,z, label="parametric curve")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

# Create 3D Scatter plot
def create_3d_scatter(n = 100):
    np.random.seed(19680801) # Seed taken from https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html documentation

    fig = plt.figure() # the 'canvas'
    ax = fig.add_subplot(projection="3d") # the 'drawing'

    for m, zlow, zhigh in [("o", -50, -25), ("^", 25, 50)]:
        xs = randrange(n, 0, 25)
        ys = randrange(n, 0, 100)
        zs = randrange(n, zlow, zhigh)
        ax.scatter(xs, ys, zs, marker=m)  

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    create_gif(fig, ax, "scatter_plot", degree=2, elevation=10)

# Create 3D Surface plot
def create_3d_surface():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Setup data for the meshgrid
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)

    X, Y = np.meshgrid(x, y) 
    Z = surface_function(X, Y)

    surf = ax.plot_surface(X, Y, Z,          # data
                           cmap="viridis",   # viridis colors the carpet by elevation
                           linewidth=0,      # removes ugly border lines
                           alpha=0.75,        # make that line more visible, bang
                           zorder=1,         # try z-order to make line more visible
                           antialiased=True) # Smooths the rendered edges

    fig.colorbar(surf,                  # mapable obj
                 ax=ax,                 # reference the 'drawing'
                 shrink=0.5,            # make the bar half the size of the fig
                 aspect=10,             # higher = thinner bar, vice versa
                 label="Z Elevation")   # label on the color bar

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Elevation)')
    ax.set_title("3D Surface")

    # Create the lines ON the surface - later helpful for adding the descent
    # Start with something basic like slicing the surface
    x_slice = np.linspace(-10, 10, 200) # 200 in the middle of that sweet spot from notes
    y_slice = np.zeros_like(x_slice)    # y=0
    z_slice = surface_function(x_slice, y_slice)

    ax.plot(x_slice, y_slice, z_slice + 0.015, # data, + 0.015 is to help line be more visible and avoid Z-fighting
            color='r',
            linewidth=3,
            zorder=10,
            alpha=0.8,
            label="Slice of surface (y=0)")

    # add a spiral-like line now
    theta = np.linspace(0, 4*np.pi, 200)
    rad_spiral = np.linspace(0.2, 9.8, 200) # so the spiral can grow in and out of the graph

    x_spiral = rad_spiral * np.cos(theta)
    y_spiral = rad_spiral * np.sin(theta)
    z_spiral = surface_function(x_spiral, y_spiral)

    ax.plot(x_spiral, y_spiral, z_spiral + 0.015,
            color = "k",
            linewidth = 3,
            zorder = 10,
            alpha=0.8,
            label="Spiral on surface")

    create_gif(fig, ax, "surface_plot", degree=1)


if __name__ == "__main__":
    # create_3d_line()
    # create_3d_scatter()
    create_3d_surface()