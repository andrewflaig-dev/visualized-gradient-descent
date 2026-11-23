import matplotlib
import matplotlib.pyplot as plt
import plot_creation
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

def perform_gradient_descent(fig, ax, z_func, lr=0.05, threshold = 100):
    x_start = ((ax.get_xlim()[1] * 2) * np.random.rand()) + ax.get_xlim()[0]
    y_start = (ax.get_ylim()[1] * 2) * np.random.rand() + ax.get_ylim()[0]
    z_start = z_func(x_start, y_start)

    ax.scatter(x_start, y_start, z_start + 0.05)

    x_path = [x_start]
    y_path = [y_start]
    z_path = [z_start]

    # Initialize values
    curr_x = x_start
    curr_y = y_start
    curr_z = z_start

    grad = np.array([2*curr_x, 2*curr_y])

    for _ in range(threshold):
        curr_coord = np.array([curr_x, curr_y])
        curr_x, curr_y = curr_coord - lr * grad
        curr_z = z_func(curr_x, curr_y)

        # add to paths
        x_path.append(curr_x)
        y_path.append(curr_y)
        z_path.append(curr_z)

        grad = np.array([2*curr_x, 2*curr_y])

    grad_line, = ax.plot([], [], [],      # Starts empty so x,y,z must be empty
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
        curr_x_trail = x_path[:frame+1]
        curr_y_trail = y_path[:frame+1]
        curr_z_trail = z_path[:frame+1]

        grad_line.set_data(curr_x_trail, curr_y_trail)
        grad_line.set_3d_properties(curr_z_trail)

        lead_point.set_data([x_path[frame]], [y_path[frame]])
        lead_point.set_3d_properties([z_path[frame]])

    anim = FuncAnimation(
        fig,
        update,
        frames=threshold,
        interval=33,
        blit=False,
        repeat=True
    )

    anim.save("images/grad_decent_on_paraboloid.gif", writer="pillow", fps=60)


if __name__ == "__main__":
    # fig, ax, z_func = plot_creation.paraboloid()
    # perform_gradient_descent(fig, ax, z_func)
