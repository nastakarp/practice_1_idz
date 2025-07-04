import tkinter as tk
from tkinter import ttk, colorchooser
import numpy as np
from math import sin, cos, pi


class RoseAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Движение пятиугольника по розе")

        self.a = 150
        self.t = 0
        self.step = 0.05
        self.repeats = 0
        self.max_repeats = 0
        self.pulse_min = 20
        self.pulse_max = 60
        self.pulse_speed = 0.5
        self.pulse_value = 40
        self.pulse_direction = 1
        self.direction = 1
        self.obj_color = "red"
        self.path_color = "blue"
        self.obj_style = "solid"
        self.rotation_angle = 0  # Угол вращения объекта
        self.rotation_speed = 0  # Скорость вращения объекта

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_controls()
        self.draw_rose()
        self.animation_id = None

    def create_controls(self):
        tk.Button(self.control_frame, text="Старт", width=20, command=self.start_animation).pack(pady=3)
        tk.Button(self.control_frame, text="Стоп", width=20, command=self.stop_animation).pack(pady=3)

        tk.Button(self.control_frame, text="Цвет объекта", width=20, command=self.choose_obj_color).pack(pady=3)
        tk.Button(self.control_frame, text="Цвет траектории", width=20, command=self.choose_path_color).pack(pady=3)

        self.obj_width_entry = self.add_labeled_entry("Толщина объекта:", "2")
        self.path_width_entry = self.add_labeled_entry("Толщина траектории:", "2", callback=self.draw_rose)

        self.obj_style_combo = self.add_labeled_combobox("Стиль объекта:", ["solid", "dashed", "dotted"], "solid")
        self.path_style_combo = self.add_labeled_combobox(
            "Стиль траектории:", ["solid", "dashed", "dotted"], "solid"
        )
        self.path_style_combo.bind("<<ComboboxSelected>>", lambda e: self.draw_rose())

        self.pulse_speed_entry = self.add_labeled_entry("Скор. пульсации:", "0.5")
        self.pulse_min_entry = self.add_labeled_entry("Мин. размер:", "20")
        self.pulse_max_entry = self.add_labeled_entry("Макс. размер:", "60")

        self.speed_entry = self.add_labeled_entry("Скорость движения:", "0.05")
        self.repeat_entry = self.add_labeled_entry("Число повторов:", "0")
        self.direction_combo = self.add_labeled_combobox("Направление:", ["по часовой", "против часовой"], "по часовой")

        # Добавлен элемент управления для скорости вращения
        self.rotation_speed_entry = self.add_labeled_entry("Скорость вращения:", "0")

        self.pent_width_entry = self.add_labeled_entry("Ширина фигуры:", "40")
        self.pent_height_entry = self.add_labeled_entry("Высота фигуры:", "30")

        self.anchor_combo = self.add_labeled_combobox(
            "Привязка:", ["центр", "правая вершина"], "центр"
        )

    def add_labeled_entry(self, text, default, callback=None):
        frame = tk.Frame(self.control_frame)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=text).pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=7)
        entry.insert(0, default)
        entry.pack(side=tk.RIGHT)
        if callback:
            entry.bind("<KeyRelease>", lambda e: callback())
        return entry

    def add_labeled_combobox(self, label, options, default):
        frame = tk.Frame(self.control_frame)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=label).pack(side=tk.LEFT)
        combo = ttk.Combobox(frame, values=options, width=20, state="readonly")
        combo.set(default)
        combo.pack(side=tk.RIGHT)
        return combo

    def choose_obj_color(self):
        color = colorchooser.askcolor(title="Цвет объекта")[1]
        if color:
            self.obj_color = color

    def choose_path_color(self):
        color = colorchooser.askcolor(title="Цвет траектории")[1]
        if color:
            self.path_color = color
            self.draw_rose()

    def draw_rose(self):
        self.canvas.delete("rose")
        style = self.path_style_combo.get()
        dash = self.get_dash_pattern(style)
        path_width = self.get_float(self.path_width_entry, 2)

        points = []
        for phi in np.linspace(0, 2 * pi, 300):
            r = self.a * sin(3 * phi)
            x = 300 + r * cos(phi)
            y = 300 + r * sin(phi)
            points.extend([x, y])

        self.canvas.create_line(
            *points,
            fill=self.path_color,
            width=path_width,
            tags="rose",
            dash=dash
        )

    def get_dash_pattern(self, style):
        return {
            "solid": None,
            "dashed": (10, 5),
            "dotted": (2, 4)
        }.get(style, None)

    def get_float(self, entry, default):
        try:
            return float(entry.get())
        except ValueError:
            return default

    def rotate_point(self, point, center, angle):
        """Вращает точку вокруг центра на заданный угол"""
        ox, oy = center
        px, py = point

        qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
        qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)

        return qx, qy

    def get_pentagon_points(self, x, y, width=40, height=30, anchor="центр"):
        half_w = width / 2
        half_h = height / 2

        if anchor == "центр":
            cx, cy = x, y
        elif anchor == "правая вершина":
            cx = x - (half_w + width * 0.6)
            cy = y
        else:
            cx, cy = x, y

        # Построение фигуры
        top_left = (cx - half_w, cy - half_h)
        bottom_left = (cx - half_w, cy + half_h)
        bottom_right = (cx + half_w, cy + half_h)
        top_right = (cx + half_w, cy - half_h)
        right_peak = (cx + half_w + width * 0.6, cy)

        points = [top_left, bottom_left, bottom_right, right_peak, top_right]

        # Применяем вращение, если скорость вращения не нулевая
        if self.rotation_speed != 0:
            center = (cx, cy)
            rotated_points = []
            for point in points:
                rotated_point = self.rotate_point(point, center, self.rotation_angle)
                rotated_points.append(rotated_point)
            points = rotated_points

        # Преобразуем список точек в плоский список координат
        flat_points = []
        for point in points:
            flat_points.extend(point)

        return flat_points

    def update_animation(self):
        if self.animation_id is None:
            return

        self.canvas.delete("pentagon")

        self.step = self.get_float(self.speed_entry, 0.05)
        self.direction = 1 if self.direction_combo.get() == "по часовой" else -1
        self.max_repeats = int(self.repeat_entry.get()) if self.repeat_entry.get().isdigit() else 0

        # Обновляем скорость вращения
        self.rotation_speed = self.get_float(self.rotation_speed_entry, 0)
        self.rotation_angle += self.rotation_speed * pi / 180  # Преобразуем градусы в радианы

        # Пульсация
        self.pulse_min = self.get_float(self.pulse_min_entry, 20)
        self.pulse_max = self.get_float(self.pulse_max_entry, 60)
        self.pulse_speed = self.get_float(self.pulse_speed_entry, 0.5)
        self.pulse_value += self.pulse_direction * self.pulse_speed
        if self.pulse_value >= self.pulse_max or self.pulse_value <= self.pulse_min:
            self.pulse_direction *= -1

        # Координаты на траектории
        r = self.a * sin(3 * self.t)
        x = 300 + r * cos(self.t)
        y = 300 + r * sin(self.t)

        # Параметры фигуры
        width = self.get_float(self.pent_width_entry, 40)
        height = self.get_float(self.pent_height_entry, 30)
        anchor = self.anchor_combo.get()

        dash = self.get_dash_pattern(self.obj_style_combo.get())
        outline_width = self.get_float(self.obj_width_entry, 2)

        points = self.get_pentagon_points(
            x, y,
            self.pulse_value,
            self.pulse_value * height / width,
            anchor
        )

        self.canvas.create_polygon(
            *points,
            fill=self.obj_color,
            outline="black",
            dash=dash,
            width=outline_width,
            tags="pentagon"
        )

        # Обновление угла
        self.t += self.step * self.direction
        if self.t > 2 * pi:
            self.t -= 2 * pi
            self.repeats += 1
        elif self.t < 0:
            self.t += 2 * pi
            self.repeats += 1

        if self.max_repeats > 0 and self.repeats >= self.max_repeats:
            self.stop_animation()
        else:
            self.animation_id = self.root.after(50, self.update_animation)

    def start_animation(self):
        if self.animation_id is None:
            self.repeats = 0
            self.t = 0
            self.rotation_angle = 0  # Сбрасываем угол вращения
            self.animation_id = self.root.after(0, self.update_animation)

    def stop_animation(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None


if __name__ == "__main__":
    root = tk.Tk()
    app = RoseAnimation(root)
    root.mainloop()