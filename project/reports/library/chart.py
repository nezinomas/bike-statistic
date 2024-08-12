colors = [
    (255, 99, 132),
    (54, 162, 235),
    (255, 206, 86),
    (38, 85, 238),
    (153, 102, 255),
    (27, 158, 1),
    (200, 200, 200),
]


def get_color(num, alpha=1):
    if num >= len(colors):
        num = len(colors) - 1

    red = colors[num][0]
    blue = colors[num][1]
    green = colors[num][2]

    return f"rgba({red}, {blue}, {green}, {alpha})"
