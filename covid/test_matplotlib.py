import matplotlib; matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

k = 2 * np.pi
w = 2 * np.pi
dt = 0.01

xmin = 0
xmax = 3
nbx = 100

x = np.linspace(xmin, xmax, nbx)

fig = plt.figure()  # initialise la figure
line, = plt.plot([], [])
plt.xlim(xmin, xmax)
plt.ylim(-1, 1)


# fonction à définir quand blit=True
# crée l'arrière de l'animation qui sera présent sur chaque image
def init():
    line.set_data([], [])
    return line,


def animate(i):
    t = i * dt
    y = np.cos(k * x - w * t)
    line.set_data(x, y)
    return line,


ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=100,
                              init_func=init,
                              blit=True,
                              interval=20,  # delay between frames
                              repeat=False)

plt.show()
