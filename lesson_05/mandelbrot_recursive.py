import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def mandelbrot_recursive(c, z=complex(0, 0), iteration=0, max_iter=100):
    """
    Рекурсивна функція для перевірки, чи належить точка c множині Мандельброта.

    Args:
        c (complex): Комплексне число, що представляє точку на площині
        z (complex): Поточне значення z (за замовчуванням 0)
        iteration (int): Поточна ітерація (за замовчуванням 0)
        max_iter (int): Максимальна кількість ітерацій

    Returns:
        int: Кількість ітерацій до втечі або max_iter, якщо точка в множині
    """
    if iteration >= max_iter or abs(z) > 2:
        return iteration

    z_next = z * z + c
    return mandelbrot_recursive(c, z_next, iteration + 1, max_iter)

def generate_mandelbrot(width=800, height=600, x_min=-2.5, x_max=1.5, y_min=-1.5, y_max=1.5, max_iter=100):
    """
    Генерує зображення множини Мандельброта.

    Args:
        width (int): Ширина зображення
        height (int): Висота зображення
        x_min, x_max, y_min, y_max (float): Межі області перегляду
        max_iter (int): Максимальна кількість ітерацій

    Returns:
        numpy.ndarray: Масив значень ітерацій для кожної точки
    """
    image = np.zeros((height, width))

    # Створюємо сітку точок
    x_values = np.linspace(x_min, x_max, width)
    y_values = np.linspace(y_min, y_max, height)

    for i, y in enumerate(y_values):
        for j, x in enumerate(x_values):
            c = complex(x, y)
            image[i, j] = mandelbrot_recursive(c, max_iter=max_iter)

    return image

def plot_mandelbrot(image, title="Множина Мандельброта"):
    """
    Відображає множину Мандельброта з красивими кольорами.

    Args:
        image (numpy.ndarray): Масив значень ітерацій
        title (str): Заголовок графіка
    """
    # Створюємо кольорову карту
    cmap = plt.cm.get_cmap('inferno').reversed()
    norm = mcolors.PowerNorm(gamma=0.3, vmin=0, vmax=np.max(image))

    plt.figure(figsize=(12, 9))
    plt.imshow(image, extent=(-2.5, 1.5, -1.5, 1.5), cmap=cmap, norm=norm, interpolation='bilinear')
    plt.colorbar(label='Кількість ітерацій')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.grid(False)
    plt.tight_layout()
    plt.savefig('mandelbrot_beautiful.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """
    Головна функція для генерації та відображення множини Мандельброта.
    """
    print("Генерація множини Мандельброта...")

    # Генеруємо зображення
    mandelbrot_image = generate_mandelbrot(width=1000, height=800, max_iter=200)

    # Відображаємо результат
    plot_mandelbrot(mandelbrot_image)

    print("Зображення збережено як 'mandelbrot_beautiful.png'")

if __name__ == "__main__":
    main()
