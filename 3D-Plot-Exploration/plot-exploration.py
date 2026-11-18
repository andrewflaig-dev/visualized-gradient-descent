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
    # Learning animation and how to save to files
    anim = FuncAnimation(fig, lambda a: ax.view_init(elev=elevation, azim=a),
                        frames=range(0, 360, degree))
    anim.save(f"images/{file_name}.gif", writer=PillowWriter(fps=fps))

    plt.close(fig) # Save Memory

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

# Create 3D Wirefram plot
def create_3d_wireframe():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # Setup data for the meshgrid
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)

    X, Y = np.meshgrid(x, y) 

    # For practice, I'm going to make a ripple cause it looks cool [Z = sin(sqrt(X^2 + Y^2)) / sqrt(X^2 + Y^2))]
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R) / (R + 1e-5) # 1e-5 is to avoid dividing by zero

    surf = ax.plot_surface(X, Y, Z, 
                           cmap="viridis",   # viridis colors the carpet by elevation
                           linewidth=0,       # removes ugly border lines
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

    create_gif(fig, ax, "surface_plot", degree=1)

if __name__ == "__main__":
    # create_3d_line()
    # create_3d_scatter()
    # create_3d_wireframe()