from math import dist

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def z(t, j, points):
    return sum((
        points[k][j] * comb(len(points) - 1, k) * (t ** k) * ((1 - t) ** (len(points) - 1 - k))
        for k in range(len(points))
    ))

def B(t, points):
    return np.array([
        z(t, 0, points),
        z(t, 1, points),
    ])

def get_curve(points, num_points=100):
    return np.array([B(t, points) for t in np.linspace(0, 1, num_points)])

def generate_random_dots(start, end, num_mid_points, aspect=1.0, alpha_jitter=0.1):
    start = np.array(start)
    end = np.array(end)
    d = (end - start) / dist(start, end)
    n = np.array([-d[1], d[0]])

    spread = dist(start, end) * aspect
    alpha_spray = 1 / (num_mid_points + 1)

    # --- borders ---
    global border
    border = [
        start + n * spread,
        end + n * spread,
        end - n * spread,
        start - n * spread,
        start + n * spread,
    ]

    # --- random points ---

    result = [start]
    for i in range(num_mid_points):
        alpha_noise = np.random.random() * alpha_jitter * (2 * alpha_spray) - alpha_spray * alpha_jitter
        alpha = (i + 1) / (num_mid_points + 1) + alpha_noise
        beta = np.random.random() * (spread * 2) - spread

        result.append(d * alpha * dist(start, end) + start + n * beta)

    result.append(end)
    return result


def plot_cpp_solution():
    global plt
    with open(f"../../CProjects/TraceBezierCurve/out", "r") as file:
        x, y = [], []
        for line in file.readlines():
            a, b = map(float, line.split())
            if a == 0 and b == 0 and x:
                break
            x.append(a)
            y.append(b)
        plt.plot(x, y, 'm')


border = []
points = generate_random_dots([0, 0],
                              [5, 5.5],
                              num_mid_points=5,
                              aspect=0.2,
                              alpha_jitter=0.1)

# points = np.array([
#     [0, 0],
#     [1, 4],
#     [2, 1],
#     [3, 3],
#     [4, 2],
#     [3, 1],
# ])

plt.figure(figsize=(8, 8))
curve = get_curve(points, num_points=50)
# plt.xlim(-1, 6)
# plt.ylim(-1, 6)
plt.plot(*zip(*points), 'ro', label='Control Points')
plt.plot(*zip(*curve), 'b-', label='Bezier Curve')
plt.plot(*zip(*border), 'g--', label='Border')
plot_cpp_solution()
plt.show()

