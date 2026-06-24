import tkinter as tk
import glob
import time

class ZeroTwoBongo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zero Two Bongo")
        self.root.configure(bg="black")
        self.root.overrideredirect(True)

        self.root.geometry("300x300+100+100")

        # загружаем все кадры zero_two_*.png
        self.frames = []
        for path in sorted(glob.glob("zero_two_*.png")):
            self.frames.append(tk.PhotoImage(file=path))

        if not self.frames:
            raise RuntimeError("Не найдены файлы zero_two_*.png. Положи их рядом со скриптом.")

        self.current_frame_index = 0
        self.last_frame_change_time = time.time()

        self.base_speed = 0.12
        self.current_speed = self.base_speed

        self.label = tk.Label(self.root, bg="black")
        self.label.pack(expand=True)

        self.score = 0
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", fg="white", bg="black")
        self.score_label.pack()

        self.root.bind("<KeyPress>", self.on_key_press)

        self.update_animation()
        self.root.mainloop()

    def on_key_press(self, event):
        self.score += 1
        self.score_label.config(text=f"Score: {self.score}")
        self.current_speed = max(0.04, self.current_speed * 0.7)

    def update_animation(self):
        now = time.time()
        if now - self.last_frame_change_time >= self.current_speed:
            self.last_frame_change_time = now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.label.config(image=self.frames[self.current_frame_index])

            if self.current_speed < self.base_speed:
                self.current_speed += 0.01

        self.root.after(10, self.update_animation)


if __name__ == "__main__":
    ZeroTwoBongo()