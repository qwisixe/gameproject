import tkinter as tk
from PIL import Image, ImageTk  # нужна Pillow
import time
from itertools import count

GIF_PATH = "zero_two.gif"  # твоя гифка

class ZeroTwoBongo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zero Two Bongo")
        self.configure(bg="black")
        self.overrideredirect(True)
        self.geometry("300x300+100+100")

        # Загружаем GIF через Pillow
        try:
            pil_image = Image.open(GIF_PATH)
        except Exception as e:
            raise RuntimeError(f"Не удалось открыть GIF {GIF_PATH}: {e}")

        self.frames = []
        # соберём все кадры
        try:
            for i in count(0):
                pil_image.seek(i)
                frame = ImageTk.PhotoImage(pil_image.copy())
                self.frames.append(frame)
        except EOFError:
            pass

        if not self.frames:
            raise RuntimeError("GIF не содержит кадров или не поддерживается.")

        # состояние анимации
        self.current_frame_index = 0
        self.base_delay = pil_image.info.get("duration", 100) / 1000.0  # мс -> секунды [web:74]
        self.current_delay = self.base_delay

        # виджет
        self.label = tk.Label(self, bg="black")
        self.label.pack(expand=True)

        # счётчик
        self.score = 0
        self.score_label = tk.Label(self, text=f"Score: {self.score}", fg="white", bg="black")
        self.score_label.pack()

        # биндим клавиши
        self.bind("<KeyPress>", self.on_key_press)

        # запускаем анимацию
        self.last_change = time.time()
        self.animate()

    def on_key_press(self, event):
        # "удар" по бонго — ускоряем анимацию и добавляем очки
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.current_delay = max(0.04, self.current_delay * 0.7)

    def animate(self):
        now = time.time()
        if now - self.last_change >= self.current_delay:
            self.last_change = now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.label.config(image=self.frames[self.current_frame_index])

            # медленно возвращаемся к базовой скорости
            if self.current_delay < self.base_delay:
                self.current_delay += 0.01

        self.after(10, self.animate)


if __name__ == "__main__":
    app = ZeroTwoBongo()
    app.mainloop()