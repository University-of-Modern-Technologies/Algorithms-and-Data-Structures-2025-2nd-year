def fill_color(matrix, x, y, old_color, new_color):
    if (x < 0 or x >= len(matrix)) or (y < 0 or y >= len(image[0])) or matrix[x][y] != old_color:
        return


    image[x][y] = new_color

    fill_color(matrix, x + 1, y, old_color, new_color)
    fill_color(matrix, x - 1, y, old_color, new_color)
    fill_color(matrix, x, y + 1, old_color, new_color)
    fill_color(matrix, x, y - 1, old_color, new_color)


image = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 0],
]

fill_color(image, 1, 2, 0, 2)
for row in image:
    print(row)
