import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import os

MAIN_GIF = "zero_two.gif"
ALT_GIF = "zero_two_alt.gif"
SCORE_FILE = "score.txt"
UPGRADE_FILE = "upgrades.txt"


class ZeroTwoGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Zero Two Bongo")
        self.geometry("640x640+100+100")
        self.minsize(640, 640)
        self.maxsize(640, 640)
        self.configure(bg="#ffb6c1")

        self.score = self.load_score()
        self.multiplier, self.auto_interval_ms, self.use_alt_skin, self.anim_speed_factor = self.load_upgrades()

        self.current_frame = None

        self.create_start_screen()

    # ===== стартовый экран =====

    def create_start_screen(self):
        self._switch_frame(bg="#ffb6c1")

        title = tk.Label(
            self.current_frame,
            text="Zero Two Bongo",
            fg="#1b1b2f",
            bg="#ffb6c1",
            font=("Arial", 26, "bold"),
        )
        title.pack(pady=60)

        play_button = tk.Button(
            self.current_frame,
            text="Играть",
            command=self.start_game,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=3,
            font=("Arial", 18, "bold"),
            cursor="hand2",
            padx=40,
            pady=10,
        )
        play_button.pack(pady=20)

        dev_button = tk.Button(
            self.current_frame,
            text="Разработчики",
            command=self.show_devs,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=3,
            font=("Arial", 18, "bold"),
            cursor="hand2",
            padx=40,
            pady=10,
        )
        dev_button.pack(pady=20)

    def show_devs(self):
        self._switch_frame(bg="#ffb6c1")

        label = tk.Label(
            self.current_frame,
            text="Главный разработчик - qwisixe",
            fg="red",
            bg="#ffb6c1",
            font=("Arial", 22, "bold"),
        )
        label.pack(expand=True)

        back_button = tk.Button(
            self.current_frame,
            text="Назад",
            command=self.create_start_screen,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=3,
            font=("Arial", 14, "bold"),
            cursor="hand2",
            padx=20,
            pady=5,
        )
        back_button.pack(pady=20)

    # ===== запуск игры =====

    def start_game(self):
        # при заходе в игру сбрасываем auto_click_running
        self.auto_click_running = False

        self._switch_frame(bg="#1b1b2f")

        # область с GIF
        self.image_label = tk.Label(self.current_frame, bg="#1b1b2f")
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # нижняя панель
        self.panel = tk.Frame(self.current_frame, bg="#ff69b4", height=80)
        self.panel.pack(fill=tk.X, side=tk.BOTTOM)

        # загрузка кадров GIF
        self.load_gif_frames()

        # счёт
        self.score_label = tk.Label(
            self.panel,
            text=self.score_text(),
            fg="white",
            bg="#ff69b4",
            font=("Arial", 14, "bold"),
        )
        self.score_label.pack(side=tk.LEFT, padx=10)

        # кнопка Hit
        self.hit_button = tk.Button(
            self.panel,
            text="Hit!",
            command=self.on_hit,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=3,
            font=("Arial", 14, "bold"),
            cursor="hand2",
            padx=20,
            pady=5,
        )
        self.hit_button.pack(side=tk.RIGHT, padx=10)

        # кнопка Shop
        self.shop_button = tk.Button(
            self.panel,
            text="Shop",
            command=self.open_shop,
            fg="#1b1b2f",
            bg="#ffc0cb",
            activebackground="#ffdde8",
            activeforeground="#1b1b2f",
            relief="ridge",
            bd=2,
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=10,
            pady=3,
        )
        self.shop_button.pack(side=tk.LEFT, padx=10)

        # кнопка Меню (выход в главное меню)
        self.menu_button = tk.Button(
            self.panel,
            text="Меню",
            command=self.back_to_menu,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=10,
            pady=3,
        )
        self.menu_button.pack(side=tk.LEFT, padx=10)

        self.bind("<KeyPress>", self.on_key_press)

        self.current_frame_index = 0
        self.animate()
        self.start_auto_clicker()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def back_to_menu(self):
        # сохраняем прогресс и возвращаем в главное меню
        self.save_score()
        self.save_upgrades()
        self.create_start_screen()

    # ===== вспомогательное для экранов =====

    def _switch_frame(self, bg):
        if self.current_frame is not None:
            self.current_frame.destroy()
        frame = tk.Frame(self, bg=bg)
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

    # ===== GIF =====

    def load_gif_frames(self):
        # безопаная смена скина
        if self.use_alt_skin and os.path.exists(ALT_GIF):
            gif_path = ALT_GIF
            alt_mode = True
        else:
            gif_path = MAIN_GIF
            alt_mode = False

        try:
            pil_image = Image.open(gif_path)
        except Exception as e:
            raise RuntimeError(f"Не удалось открыть GIF {gif_path}: {e}")

        self.frames = []
        try:
            for i in count(0):
                pil_image.seek(i)
                frame = pil_image.copy().resize((400, 400))
                photo = ImageTk.PhotoImage(frame)
                self.frames.append(photo)
        except EOFError:
            pass

        if not self.frames:
            raise RuntimeError("GIF не содержит кадров или не поддерживается.")

        base_delay = pil_image.info.get("duration", 100) / 1000.0

        # если ALT‑скин, делаем его быстрее, чем обычный
        speed_factor = self.anim_speed_factor
        if alt_mode:
            speed_factor *= 1.5  # доп. ускорение для альтернативного скина

        self.base_delay = max(0.02, base_delay / speed_factor)

    def animate(self):
        if not hasattr(self, "frames") or not self.frames:
            return
        self.image_label.config(image=self.frames[self.current_frame_index])
        self.image_label.image = self.frames[self.current_frame_index]

        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        delay_ms = int(self.base_delay * 1000)
        self.after(delay_ms, self.animate)

    # ===== сохранение / загрузка =====

    def load_score(self):
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r", encoding="utf-8") as f:
                    val = f.read().strip()
                    if val:
                        return int(val)
            except Exception:
                return 0
        return 0

    def save_score(self):
        try:
            with open(SCORE_FILE, "w", encoding="utf-8") as f:
                f.write(str(self.score))
        except Exception:
            pass

    def load_upgrades(self):
        default = (1.0, 0, False, 1.0)
        if os.path.exists(UPGRADE_FILE):
            try:
                with open(UPGRADE_FILE, "r", encoding="utf-8") as f:
                    line = f.read().strip()
                    if line:
                        parts = line.split(";")
                        mult = float(parts[0])
                        auto_ms = int(parts[1])
                        use_alt = parts[2] == "1"
                        anim_speed = float(parts[3])
                        return mult, auto_ms, use_alt, anim_speed
            except Exception:
                return default
        return default

    def save_upgrades(self):
        try:
            with open(UPGRADE_FILE, "w", encoding="utf-8") as f:
                use_alt_flag = "1" if self.use_alt_skin else "0"
                f.write(f"{self.multiplier};{self.auto_interval_ms};{use_alt_flag};{self.anim_speed_factor}")
        except Exception:
            pass

    def score_text(self):
        return f"Score: {self.score}  (x{self.multiplier:.1f})"

    def update_score_label(self):
        self.score_label.config(text=self.score_text())

    def add_score(self, amount):
        gained = int(amount * self.multiplier)
        self.score += gained
        self.update_score_label()

    # ===== события =====

    def on_hit(self):
        self.add_score(1)

    def on_key_press(self, event):
        self.add_score(1)

    def on_close(self):
        self.save_score()
        self.save_upgrades()
        self.destroy()

    # ===== авто-кликер =====

    def start_auto_clicker(self):
        if self.auto_interval_ms and self.auto_interval_ms > 0:
            self.auto_click_running = True
            self.after(self.auto_interval_ms, self.auto_click_tick)

    def auto_click_tick(self):
        if not self.auto_click_running:
            return
        self.add_score(1)
        self.after(self.auto_interval_ms, self.auto_click_tick)

    # ===== магазин =====

    def open_shop(self):
        shop = tk.Toplevel(self)
        shop.title("Shop")
        shop.geometry("360x400+760+120")
        shop.configure(bg="#ffb6c1")

        info = tk.Label(
            shop,
            text=self.shop_info_text(),
            fg="#1b1b2f",
            bg="#ffb6c1",
            font=("Arial", 11),
            justify="left",
        )
        info.pack(pady=10)

        btn_x2 = tk.Button(
            shop,
            text="Купить x2 множитель (100 Score)",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.buy_multiplier(shop, info, 2.0, 100),
        )
        btn_x2.pack(pady=5)

        btn_x4 = tk.Button(
            shop,
            text="Купить x4 множитель (250 Score)",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.buy_multiplier(shop, info, 4.0, 250),
        )
        btn_x4.pack(pady=5)

        btn_auto = tk.Button(
            shop,
            text="Автокликер / ускорение (150 Score)",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.buy_autoclick(shop, info, 150),
        )
        btn_auto.pack(pady=5)

        btn_skin = tk.Button(
            shop,
            text="Сменить скин на ALT (200 Score)",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.buy_skin(shop, info, 200),
        )
        btn_skin.pack(pady=5)

        # инвентарь скинов (выбор MAIN/ALT без покупки)
        btn_inventory = tk.Button(
            shop,
            text="Инвентарь скинов",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.open_skin_inventory(shop, info),
        )
        btn_inventory.pack(pady=5)

        btn_anim = tk.Button(
            shop,
            text="Ускорить анимацию (x1.5) (120 Score)",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.buy_anim_speed(shop, info, 120),
        )
        btn_anim.pack(pady=5)

        close_btn = tk.Button(
            shop,
            text="Закрыть",
            command=shop.destroy,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
        )
        close_btn.pack(pady=10)

    def shop_info_text(self):
        return (
            f"Score: {self.score}\n"
            f"Множитель: x{self.multiplier:.1f}\n"
            f"Автокликер: "
            f"{'ON (' + str(self.auto_interval_ms) + ' ms)' if self.auto_interval_ms else 'OFF'}\n"
            f"Скин: {'ALT' if self.use_alt_skin else 'MAIN'}\n"
            f"Скорость анимации: x{self.anim_speed_factor:.1f}"
        )

    def refresh_shop_info(self, label):
        label.config(text=self.shop_info_text())

    def buy_multiplier(self, shop_window, info_label, factor, cost):
        if self.score >= cost:
            self.score -= cost
            self.multiplier *= factor
            self.update_score_label()
            self.save_score()
            self.save_upgrades()
            self.refresh_shop_info(info_label)
            msg = tk.Label(
                shop_window,
                text=f"Множитель увеличен! Теперь x{self.multiplier:.1f}.",
                fg="#1b1b2f",
                bg="#ffb6c1",
                font=("Arial", 11),
            )
            msg.pack(pady=3)
        else:
            self._not_enough_score(shop_window)

    def buy_autoclick(self, shop_window, info_label, cost):
        if self.score >= cost:
            self.score -= cost
            if not self.auto_interval_ms:
                self.auto_interval_ms = 1000
                self.start_auto_clicker()
            else:
                self.auto_interval_ms = max(200, int(self.auto_interval_ms * 0.7))
            self.update_score_label()
            self.save_score()
            self.save_upgrades()
            self.refresh_shop_info(info_label)
            msg = tk.Label(
                shop_window,
                text=f"Автокликер улучшен! Интервал: {self.auto_interval_ms} ms.",
                fg="#1b1b2f",
                bg="#ffb6c1",
                font=("Arial", 11),
            )
            msg.pack(pady=3)
        else:
            self._not_enough_score(shop_window)

    def buy_skin(self, shop_window, info_label, cost):
        if self.score >= cost:
            self.score -= cost
            self.use_alt_skin = True
            self.load_gif_frames()
            self.update_score_label()
            self.save_score()
            self.save_upgrades()
            self.refresh_shop_info(info_label)
            msg = tk.Label(
                shop_window,
                text="Скин куплен! Теперь доступен ALT.",
                fg="#1b1b2f",
                bg="#ffb6c1",
                font=("Arial", 11),
            )
            msg.pack(pady=3)
        else:
            self._not_enough_score(shop_window)

    def open_skin_inventory(self, shop_window, info_label):
        inv = tk.Toplevel(shop_window)
        inv.title("Инвентарь скинов")
        inv.geometry("260x200+820+160")
        inv.configure(bg="#ffb6c1")

        title = tk.Label(
            inv,
            text="Выбор скина",
            fg="#1b1b2f",
            bg="#ffb6c1",
            font=("Arial", 14, "bold"),
        )
        title.pack(pady=10)

        btn_main = tk.Button(
            inv,
            text="MAIN",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.set_skin(inv, info_label, use_alt=False),
        )
        btn_main.pack(pady=5)

        btn_alt = tk.Button(
            inv,
            text="ALT",
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            command=lambda: self.set_skin(inv, info_label, use_alt=True),
        )
        btn_alt.pack(pady=5)

        close_btn = tk.Button(
            inv,
            text="Закрыть",
            command=inv.destroy,
            fg="white",
            bg="#ff1493",
            activebackground="#ff85c2",
            activeforeground="white",
            relief="raised",
            bd=2,
            font=("Arial", 11, "bold"),
            cursor="hand2",
        )
        close_btn.pack(pady=10)

    def set_skin(self, inv_window, info_label, use_alt):
        self.use_alt_skin = use_alt
        self.load_gif_frames()
        self.update_score_label()
        self.save_upgrades()
        self.refresh_shop_info(info_label)
        inv_window.destroy()

    def buy_anim_speed(self, shop_window, info_label, cost):
        if self.score >= cost:
            self.score -= cost
            self.anim_speed_factor *= 1.5
            self.load_gif_frames()
            self.update_score_label()
            self.save_score()
            self.save_upgrades()
            self.refresh_shop_info(info_label)
            msg = tk.Label(
                shop_window,
                text=f"Анимация ускорена! x{self.anim_speed_factor:.1f}.",
                fg="#1b1b2f",
                bg="#ffb6c1",
                font=("Arial", 11),
            )
            msg.pack(pady=3)
        else:
            self._not_enough_score(shop_window)

    def _not_enough_score(self, shop_window):
        msg = tk.Label(
            shop_window,
            text="Недостаточно Score.",
            fg="#1b1b2f",
            bg="#ffb6c1",
            font=("Arial", 11),
        )
        msg.pack(pady=3)


if __name__ == "__main__":
    app = ZeroTwoGame()
    app.mainloop()