"""
@Author: Jianchong Guo
@Time: 2023/12/8 17:00
"""

import numpy as np

a1 = 3 * np.pi
a2 = 0.1
a3 = 0.9
a4 = 0.5
a5 = 0.5
a6 = 0.3


def original_terrain():
    x = np.linspace(0, 199, 200)
    y = np.linspace(0, 199, 200)
    x, y = np.meshgrid(x, y)

    a = 10

    term1 = np.sin(y / a + a1)
    term2 = a2 * np.sin(x / a)
    term3 = a3 * np.cos(a4 * np.sqrt(y ** 2 + x ** 2) / a)
    term4 = a5 * np.sin(a5 * np.sqrt(y ** 2 + x ** 2) / a)
    term5 = a6 * np.cos(y / a)

    term = (term1 + term2 + term3 + term4 + term5) * 1000 / 10

    return term + np.max(term)
    # return term1


def mountain_terrain(yc, xc, yt, xt, h):
    x = np.linspace(0, 199, 200)
    y = np.linspace(0, 199, 200)
    x, y = np.meshgrid(x, y)

    term1 = np.exp(-((x - xc) ** 2) / xt - ((y - yc) ** 2) / yt)
    return h * term1


def terrain_three():
    z1 = original_terrain()
    z2 = mountain_terrain(45, 60, 80, 50, 1000) + mountain_terrain(90, 150, 290, 220, 2500) \
         + mountain_terrain(150, 90, 120, 260, 4300)
    z = np.maximum(z1, z2)
    return z


def terrain_four():
    z1 = original_terrain()
    z2 = mountain_terrain(50, 70, 80, 50, 2600) + mountain_terrain(80, 180, 300, 220, 3500) \
         + mountain_terrain(150, 90, 120, 250, 3200) + mountain_terrain(150, 145, 90, 60, 1500)
    z = np.maximum(z1, z2)
    return z


def terrain_eight():
    z1 = original_terrain()
    z2 = mountain_terrain(30, 70, 80, 50, 2300) + mountain_terrain(60, 100, 300, 220, 3400) \
         + mountain_terrain(150, 90, 120, 250, 3200) + mountain_terrain(100, 160, 250, 160, 4800) \
         + mountain_terrain(140, 40, 200, 50, 5300) + mountain_terrain(100, 180, 230, 50, 3800) \
         + mountain_terrain(90, 70, 150, 100, 4500) + mountain_terrain(150, 150, 90, 60, 2800)
    z = np.maximum(z1, z2)
    return z


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.ticker import MultipleLocator
    x = np.linspace(0, 199, 200)
    y = np.linspace(0, 199, 200)
    x, y = np.meshgrid(x, y)

    z = terrain_eight()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # 绘制线框
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='jet', edgecolor='None', vmin=0, vmax=5500)

    ax.set_zlim([0, 6000])

    # 设置轴标签
    ax.set_xlabel('X/km')
    ax.set_ylabel('Y/km')
    ax.set_zlabel('Z/m')

    # 添加颜色条
    fig.colorbar(surf, ax=ax, orientation='vertical', pad=0.1)

    # 设置 x 和 y 坐标轴的显示间隔
    ax.xaxis.set_major_locator(MultipleLocator(100))  # 每隔50个单位显示一个刻度
    ax.yaxis.set_major_locator(MultipleLocator(100))

    # 显示图形
    plt.show()
