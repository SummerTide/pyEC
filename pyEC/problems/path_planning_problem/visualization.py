"""
@Author: Jianchong Guo
@Time: 2023/12/14 14:57
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator


def visualization_terrain(terrain):
    z = terrain
    x_max = z.shape[0]
    y_max = z.shape[1]
    z_max = np.max(z)
    z_max = math.ceil((z_max / 500.0) + 0.001) * 500
    x = np.linspace(0, x_max - 1, x_max)
    y = np.linspace(0, y_max - 1, y_max)
    x, y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='jet', edgecolor='None', vmin=0, vmax=z_max)

    ax.set_zlim([0, z_max + 500])

    ax.set_xlabel('X/km').set_fontname('Times New Roman')
    ax.set_ylabel('Y/km', rotation=90).set_fontname('Times New Roman')
    # ax.set_zlabel('Z/m').set_fontname('Times New Roman')

    ax.xaxis.set_major_locator(MultipleLocator(100))
    ax.yaxis.set_major_locator(MultipleLocator(100))
    ax.zaxis.set_ticks([])
    # ax.axis('off')

    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    fig.colorbar(surf, ax=ax, orientation='vertical', pad=0.1)

    ax.view_init(elev=90, azim=-90)
    plt.show()
