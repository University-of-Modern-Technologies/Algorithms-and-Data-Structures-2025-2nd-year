import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class StepVisualizer:
    """Клас для покрокової візуалізації алгоритмів сортування"""
    
    def __init__(self, steps, algorithm_name="Sorting Algorithm"):
        self.steps = steps
        self.algorithm_name = algorithm_name
        self.current_step = 0
        self.total_steps = len(steps)
        
        # Налаштування фігури
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.subplots_adjust(bottom=0.2)
        
        # Створення кнопок
        ax_next = plt.axes([0.7, 0.05, 0.1, 0.075])
        ax_reset = plt.axes([0.81, 0.05, 0.1, 0.075])
        
        self.btn_next = Button(ax_next, 'Next')
        self.btn_reset = Button(ax_reset, 'Reset')
        
        self.btn_next.on_clicked(self.next_step)
        self.btn_reset.on_clicked(self.reset)
        
        # Відображення початкового стану
        self.update_plot()
        
    def update_plot(self):
        """Оновлення графіка для поточного кроку"""
        self.ax.clear()
        
        data, active_indices = self.steps[self.current_step]
        
        # Створюємо список кольорів
        colors = ['steelblue'] * len(data)
        for idx in active_indices:
            colors[idx] = 'orangered'  # активні елементи червоно-помаранчевим
        
        bars = self.ax.bar(range(len(data)), data, color=colors, edgecolor='black')
        
        # Налаштування графіка
        self.ax.set_xlabel('Index', fontsize=12)
        self.ax.set_ylabel('Value', fontsize=12)
        title = f'{self.algorithm_name} - Step {self.current_step}/{self.total_steps - 1}'
        if active_indices:
            title += f' (активні: {active_indices})'
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xticks(range(len(data)))
        
        # Додавання значень над стовпчиками
        for i, bar in enumerate(bars):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(data[i])}',
                        ha='center', va='bottom', fontsize=10)
        
        plt.draw()
        
    def next_step(self, event):
        """Перехід до наступного кроку"""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_plot()
        
    def reset(self, event):
        """Повернення до початкового стану"""
        self.current_step = 0
        self.update_plot()
        
    def show(self):
        """Показати вікно візуалізації"""
        plt.show()

