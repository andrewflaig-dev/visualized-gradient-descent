import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import rasterio

## Helper Functions
def randrange(n, vmin, vmax):
    '''
    This is to ensure that the data will fit within the constraints of the plot for the scatter plot
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
    '''
    This is for the surface function for the ripple to reduce code as I use it more than once
    '''
    # For practice, I'm going to make a ripple cause it looks cool [Z = sin(sqrt(X^2 + Y^2)) / sqrt(X^2 + Y^2))]
    R = np.sqrt(X**2 + Y**2)
    return np.sin(R) / (R + 1e-5) # 1e-5 is to avoid dividing by zero

def add_lines_to_graph(ax):
    '''
    This just helps the surface function be ambiguous
    '''
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

    return ax

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
    np.random.seed(19680801) # Seed taken from https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html documentation so I can compare ish, not really

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
def create_3d_surface(add_lines=False, animate_line=False):
    plot_name = "surface_plot"
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

    if add_lines:
        ax = add_lines_to_graph(ax=ax)
        plot_name = "surface_plot_with_lines"

    if animate_line: 
        create_animated_line(fig, ax)
        return

    create_gif(fig, ax, plot_name, degree=1)


# Create an animated line on the surface plot
def create_animated_line(fig, ax, n_frames=160):
    '''
    Picks up from the create surface plot function and finishes with a different plot
    '''
    r_path = np.linspace(9.8, 0.2, n_frames)
    theta = np.linspace(0, 6*np.pi, n_frames) # three rotations this time

    x_path = r_path * np.cos(theta)
    y_path = r_path * np.sin(theta)
    z_path = surface_function(x_path, y_path) + 0.02

    # Animation starts here, bang
    # wihtout the comma, tracer line is NOT THE LINE ITSELF, but a list containing the line
    # This is why we need the comma to unpack the tuple, ie. get the line out of it
    # this goes for lead_point as well but for a point
    tracer_line, = ax.plot([], [], [],      # Starts empty so x,y,z must be empty
                          color="crimson",
                          linewidth=3,
                          alpha=0.9,
                          zorder=10,
                          label="Decent Trajectory")

    lead_point, = ax.plot([], [], [],      # Starts empty so x,y,z must be empty
                         marker="o",
                         markersize=9,
                         markerfacecolor="silver",
                         markeredgecolor="k",
                         markeredgewidth=1.2,
                         zorder=11,
                         label="Current State")

    def update(frame):
            # slice data from frame 0 to current
            current_x_trail = x_path[:frame + 1]
            current_y_trail = y_path[:frame + 1]
            current_z_trail = z_path[:frame + 1]
    
            # update the line
            tracer_line.set_data(current_x_trail, current_y_trail)
            tracer_line.set_3d_properties(current_z_trail)

            # update leading point
            lead_point.set_data([x_path[frame]], [y_path[frame]])
            lead_point.set_3d_properties([z_path[frame]])

            return tracer_line, lead_point

    anim = FuncAnimation(
        fig,                # The canvas
        update,             # The callback function, passes the current frame number into
        frames=n_frames,    # the sequence of steps range(n_frames)
        interval=33,        # playback speed/ delay between frames (1000 ms / interval) 33 is around 30fps
        blit=False,         # must redraw the canvas
        repeat=True         # will loop once n_frames - 1 is hit
    )

    # we wont return a spinning animation as the main point is to see the line move, not the entire figure
    ax.set_title("Tracer with Leading Point")
    ax.view_init(elev=30, azim=220)
    plt.tight_layout()

    anim.save("images/tracer_animation.gif", writer="pillow", fps=30)


# Real World Data!
# Create, clean, work data
def load_smokeys_data(tif_path="smokeys_data.tif", step=3):
    with rasterio.open(tif_path) as src:
        # Read in elevation data
        Z_gsm = src.read(1).astype(float)

        # Clean Data
        nodata = src.nodata
        if nodata is not None:
            Z_gsm[Z_gsm == nodata] = np.nan
        Z_gsm[Z_gsm < 0] = np.nan

        # Downsample to improve interaction with graph
        Z_gsm = Z_gsm[::step, ::step]
        Z_gsm = Z_gsm * 3.28084 # convert to feet

        bounds = src.bounds
        x_gsm = np.linspace(bounds.left, bounds.right, Z_gsm.shape[1])
        y_gsm = np.linspace(bounds.bottom, bounds.top, Z_gsm.shape[0])
        X_gsm, Y_gsm = np.meshgrid(x_gsm, y_gsm)

        return X_gsm, Y_gsm, Z_gsm
    
# Create 3D Surface map of the Great Smokey Mountains
def create_smokeys_surface(X, Y, Z):
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    gsm = ax.plot_surface(X, Y, Z,
                          cmap=cm.terrain,
                          linewidth=0,
                          antialiased=True,
                          rstride=1, # Make sure to plot every data point
                          cstride=1)

    fig.colorbar(gsm,
                 ax=ax,
                 shrink=0.5,
                 aspect=10,
                 label="Elevation (ft)")

    ax.set_xlabel("Longitude (degrees)")
    ax.set_ylabel("Latitude (degrees)")
    ax.set_title("Great Smokey Mountains Elevation Map")

    create_gif(fig, ax, "smokeys_elevation", degree=4, fps=20)

if __name__ == "__main__":
    # create_3d_line()
    # create_3d_scatter()
    # create_3d_surface()
    # create_3d_surface(add_lines=True)
    create_3d_surface(animate_line=True)
    # X, Y, Z = load_smokeys_data()
    # create_smokeys_surface(X, Y, Z)