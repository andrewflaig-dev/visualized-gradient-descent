import matplotlib
import matplotlib.pyplot as plt
import numpy as np

## Helper Functions
def randrange(n, vmin, vmax):
    '''
    This is to ensure that the data will fit within the constraints of the plot
    '''
    return (vmax - vmin) * np.random.rand(n) + vmin

## Graph Creation 
# Create 3D parametric (line) plot
def create_3d_line():
    ax = plt.figure().add_subplot(projection="3d")

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

    plt.show()

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

    plt.show()




if __name__ == "__main__":
    # create_3d_line()
    create_3d_scatter()