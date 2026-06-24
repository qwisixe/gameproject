import tkinter as tk
from PIL import Image, ImageTk  # нужна Pillow [web:74][web:83]
from itertools import count

GIF_PATH = "zero_two.gif"  # твоя гифка рядом со скриптом

class ZeroTwoBongo(tk.Tk):
    def __init__(self):
        super().__init__()

        # окно
        self.title("Zero Two Bongo")
        self.configure(bg="black")

        # рамка, размер 640x640, позиция (100,100)
        self.geometry("640x640+100+100")  # width x height + x + y [web:106]
        self.minsize(640, 640)
        self.maxsize(640, 640)  # фиксированный размер [web:104][web:102]

        # Загружаем GIF через Pillow
        try:
            pil_image = Image.open(GIF_PATH)
        except Exception as e:
            raise RuntimeError(f"Не удалось открыть GIF {GIF_PATH}: {e}")

        # Собираем все кадры GIF
        self.frames = []
        try:
            for i in count(0):
                pil_image.seek(i)
                frame = pil_image.copy().resize((400, 400))  # подгоняем под окно, по желанию
                self.frames.append(ImageTk.PhotoImage(frame))
        except EOFError:
            pass

        if not self.frames:
            raise RuntimeError("GIF не содержит кадров или не поддерживается.")

        # задержка между кадрами (в секундах)
        self.base_delay = pil_image.info.get("duration", 100) / 1000.0  # мс → сек [web:74]
        self.current_delay = self.base_delay

        # состояние анимации
        self.current_frame_index = 0

        # виджет с картинкой
        self.image_label = tk.Label(self, bg="black")
        self.image_label.pack(expand=True)

        # счётчик "ударов"
        self.score = 0
        self.score_label = tk.Label(
            self,
            text=f"Score: {self.score}",
            fg="white",
            bg="black",
            font=("Arial", 16),
        )
        self.score_label.pack(pady=10)

        # любая клавиша = +1 очко и временное ускорение анимации
        self.bind("<KeyPress>", self.on_key_press)

        # запуск анимации
        self.animate()

    def on_key_press(self, event):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")

        # если хочешь ускорение анимации при ударе — можно добавить:
        # self.current_delay = max(self.base_delay * 0.3, self.current_delay * 0.7)

    def animate(self):
        # показываем текущий кадр
        self.image_label.config(image=self.frames[self.current_frame_index])

        # следующий кадр
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

        # планируем следующий вызов через current_delay секунд
        delay_ms = int(self.current_delay * 1000)
        self.after(delay_ms, self.animate)


if __name__ == "__main__":
    app = ZeroTwoBongo()
    app.mainloop()