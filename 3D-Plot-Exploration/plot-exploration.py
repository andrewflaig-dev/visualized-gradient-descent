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

def create_gif(fig, ax, file_name, elevation=30, degree = 3, fps=20):
    # Learning animation and how to save to files
    anim = FuncAnimation(fig, lambda a: ax.view_init(elev=elevation, azim=a),
                        frames=range(0, 360, degree))
    anim.save(f"images/{file_name}.gif", writer=PillowWriter(fps=fps))

    plt.close(fig) # Save Memory

## Graph Creation 
# Create 3D parametric (line) plot
def create_3d_line():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    theta = np.linspace(0, 10, 100)
    # Why use linspace instead of arange?
        # Arange never includes stop value and needs a step range,
        # linspace provides more accurate, predictable, and reliable data.
        # Linspace also is easier to find steps between say irrational numbers such as pi
    
    x = np.sin(theta)
    y = np.cos(theta)
    z = theta

    ax.plot(x,y,z, label="parametric curve")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

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




if __name__ == "__main__":
    # create_3d_line()
    create_3d_scatter()