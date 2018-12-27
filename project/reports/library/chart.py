colors = [
    (255, 99, 132),
    (54, 162, 235),
    (255, 206, 86),
    (75, 192, 192),
    (153, 102, 255),
    (200, 200, 200)
]


def get_color(num, alpha=1):
    if num > len(colors):
        num = len(colors)-1

    return 'rgba({r}, {b}, {g}, {alpha})'.format(
        r=colors[num][0], b=colors[num][1], g=colors[num][2], alpha=alpha)
