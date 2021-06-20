#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib as mpl
from src.utils.runge_kutta import RK
from src.utils.attractors import ATTRACTOR_PARAMS

def animate_simulation():
    fig_width = 16
    fig_height = 9
    fig_dpi = 120
    bgcolor = "#252a34"

    theme = None
    if theme:
        fig_bgcolor = theme["bgcolor"]
    else:
        fig_bgcolor = bgcolor

    mpl.use("Qt5Cairo")
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=fig_dpi)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')
    fig.set_facecolor(fig_bgcolor) 
    ax.set_facecolor(fig_bgcolor)


    attr = ATTRACTOR_PARAMS["lorenz"]
    init_coord = attr["init_coord"]
    attr_params = dict(zip(attr["params"], attr["default_params"]))
    sim_time = 50
    points = 6000
    xlim = attr["xlim"]
    ylim = attr["ylim"]
    zlim = attr["zlim"]
    

    init_coords = [init_coord]
    attractor_vects = [RK(coord, 'lorenz', attr_params) for coord in init_coords]
    for vect in attractor_vects:
        vect.RK5(0, sim_time, points)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)

    colors = plt.cm.hsv(np.linspace(0.1, 1, len(attractor_vects)))

    lines = sum([ax.plot([], [], [], '-', c=c, linewidth=1, antialiased=True)
                for c in colors], [])
    points = sum([ax.plot([], [], [], 'o', c=c)
            for c in colors], [])                   

    def init():
        for line, pt in zip(lines, points):
            line.set_data_3d([], [], [])
            pt.set_data_3d([], [], [])
        return lines + points

    def animate(i):
        steps = 4
        i = (steps * i) % len(attractor_vects[0].X)
        for line, pt, k in zip(lines, points, attractor_vects):
            if i>15000:
                line.set_data_3d(k.X[i-15000:i], k.Y[i-15000:i], k.Z[i-15000:i])
            else:
                line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
            pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
        ax.view_init(0.005 * i, 0.05 * i)
        fig.canvas.draw()
        return lines + points

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=18000//4, interval=5, blit=False)
                                
    # mywriter = animation.FFMpegWriter(bitrate=5000)
    # anim.save('test2.mp4', writer='fclearfmpeg', fps=20, extra_args=['-vcodec', 'libx264'])

    plt.show()