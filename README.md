# DiscreteBezierCurve

## Теоретическая информация

[Wikipedia](https://en.wikipedia.org/wiki/Bézier_curve)
![](https://upload.wikimedia.org/wikipedia/commons/0/0b/BezierCurve.gif)

## Построение

```python
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
  
points = np.array([  
    [0, 0],  
    [1, 4],  
    [2, 1],  
    [3, 3],  
    [4, 2],  
    [3, 1],  
])  
  
curve = get_curve(points, num_points=100)  
  
plt.plot(*zip(*points), 'ro', label='Control Points')  
plt.plot(*zip(*curve), 'b-', label='Bezier Curve')  
plt.show()
```

![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%201.png)

## Генерация промежуточных точек

#### Рандом в прямоугольнике

![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%202.svg)


```python
[def generate_random_dots(start, end, num_mid_points, margin=0.25):  
    x_min = min(start[0], end[0]) - abs(start[0] - end[0]) * margin  
    x_max = max(start[0], end[0]) + abs(start[0] - end[0]) * margin  
    y_min = min(start[1], end[1]) - abs(start[1] - end[1]) * margin  
    y_max = max(start[1], end[1]) + abs(start[1] - end[1]) * margin  
  
    result = [start]  
    for _ in range(num_mid_points):  
        x = np.random.uniform(x_min, x_max)  
        y = np.random.uniform(y_min, y_max)  
        result.append([x, y])  
    result.append(end)  
    return np.array(result)](<def generate_random_dots(start, end, num_mid_points, margin=0.25):
    x_min = min(start[0], end[0]) - abs(start[0] - end[0]) * margin
    x_max = max(start[0], end[0]) + abs(start[0] - end[0]) * margin
    y_min = min(start[1], end[1]) - abs(start[1] - end[1]) * margin
    y_max = max(start[1], end[1]) + abs(start[1] - end[1]) * margin

    result = [start]
    for _ in range(num_mid_points):
        x = x_min + np.random.random() * (x_max - x_min)
        y = y_min + np.random.random() * (y_max - y_min)
        result.append([x, y])
    result.append(end)
    return np.array(result)>)
```

![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%203.png)
![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%204.png)
![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%205.png)

Довольно не естественные флики. Попробуем другой подход

#### Канал

![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%206.svg)

Тригонометрия - это долго. Зайдём с другой стороны

![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%207.svg)

```python
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
  
  
border = []  
points = generate_random_dots([0, 0],  
                              [5, 5.5],  
                              num_mid_points=5,  
                              aspect=0.1,  
                              alpha_jitter=0.1)  
  
plt.figure(figsize=(8, 8))  
curve = get_curve(points, num_points=50)  
plt.xlim(-1, 6)  
plt.ylim(-1, 6)  
plt.plot(*zip(*points), 'ro', label='Control Points')  
plt.plot(*zip(*curve), 'b-', label='Bezier Curve')  
plt.plot(*zip(*border), 'g--', label='Border')  
plt.show()
```
![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%208.png)
![](https://raw.githubusercontent.com/Cyber-Zhaba/DiscreteBezierCurve/refs/heads/master/pictures/picture%209.png)
