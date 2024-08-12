colors = [
    (255, 99, 132),
    (54, 162, 235),
    (255, 206, 86),
    (38, 85, 238),
    (153, 102, 255),
    (27, 158, 1),
    (200, 200, 200),
]


def get_color(num: int, alpha: int = 1):
    """
    Returns an RGBA color string based on the provided index and alpha value.

    Args:
        num (int): Index of the color to retrieve.
        alpha (float, optional): Alpha value for the color. Defaults to 1.

    Returns:
        str: RGBA color string in the format "rgba(red, blue, green, alpha)".
    """
    if num >= len(colors):
        num = len(colors) - 1

    red = colors[num][0]
    blue = colors[num][1]
    green = colors[num][2]

    return f"rgba({red}, {blue}, {green}, {alpha})"
