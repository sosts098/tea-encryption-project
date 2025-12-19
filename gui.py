"""
GUI для алгоритма TEA
Автор: студент Лукьянов Александр Дмитриевич

Этот файл отвечает за графический интерфейс программы.
Здесь создаётся окно, кнопки и поля ввода.

Сам алгоритм шифрования находится в файле tea.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from tea import ecb_encrypt, ecb_decrypt

from tea import ecb_encrypt, ecb_decrypt, is_valid_hex_string


class TeaGUI:
    """
    Класс TeaGUI описывает всё окно программы.
    Можно сказать, что этот класс — это вся программа целиком.
    """

    DEFAULT_KEY = "00112233445566778899aabbccddeeff"

    def __init__(self, root):
        """
        Эта функция вызывается при запуске программы.
        Здесь создаётся окно и все элементы интерфейса.
        """
        self.root = root
        self.root.title("TEA by Александр Лукьянов")
        self.root.geometry("420x560")
        self.root.resizable(False, False)

        self.center_window()

        container = ttk.Frame(root, padding=20)
        container.pack(expand=True)

        ttk.Label(
            container,
            text="TEA by Александр Лукьянов",
            font=("Helvetica", 18, "bold")
        ).pack(pady=10)

        ttk.Label(
            container,
            text="Введите данные для шифрования",
            foreground="gray"
        ).pack(pady=5)

        # ===== ПОЛЕ ДЛЯ КЛЮЧА =====
        ttk.Label(container, text="Ключ (hex):").pack(anchor="w", pady=(20, 5))

        self.key_entry = ttk.Entry(container, width=40)
        self.key_entry.pack()
        self.key_entry.insert(0, self.DEFAULT_KEY)

        # ===== ПОЛЕ ДЛЯ ВХОДНОГО ТЕКСТА =====
        ttk.Label(container, text="Входной текст:").pack(anchor="w", pady=(15, 5))

        self.input_text = tk.Text(container, height=6, width=40)
        self.input_text.pack()

        # ===== КНОПКИ =====
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Зашифровать", command=self.encrypt)\
            .grid(row=0, column=0, padx=5)

        ttk.Button(button_frame, text="Расшифровать", command=self.decrypt)\
            .grid(row=0, column=1, padx=5)

        ttk.Button(button_frame, text="Сбросить", command=self.reset_fields)\
            .grid(row=0, column=2, padx=5)

        # ===== РЕЗУЛЬТАТ =====
        ttk.Label(container, text="Результат:").pack(anchor="w", pady=(10, 5))

        self.output_text = tk.Text(container, height=6, width=40)
        self.output_text.pack()

        ttk.Button(container, text="Выйти", command=self.exit_app).pack(pady=15)

        # Копирование и вставка
        self.add_copy_paste(self.key_entry)
        self.add_copy_paste(self.input_text)
        self.add_copy_paste(self.output_text)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    # ================== ПРОВЕРКИ ==================

    def validate_key(self):
        """
        Проверяет корректность ключа.
        """
        key_hex = self.key_entry.get().strip().replace(" ", "").lower()

        if len(key_hex) != 32:
            raise ValueError("Ключ должен содержать ровно 32 hex-символа.")

        for ch in key_hex:
            if ch not in "0123456789abcdef":
                raise ValueError("Ключ содержит недопустимые символы.")

        return bytes.fromhex(key_hex)

    def validate_input_text(self):
        """
        Проверяет, что входной текст не пустой.
        """
        text = self.input_text.get("1.0", tk.END).strip()

        if not text:
            raise ValueError("Поле «Входной текст» не может быть пустым.")

        return text

    # ================== ОСНОВНАЯ ЛОГИКА ==================

    def encrypt(self):
        """
        Шифрует введённый текст.
        """
        try:
            key = self.validate_key()
            text = self.validate_input_text()

            encrypted = ecb_encrypt(text.encode("utf-8"), key)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, encrypted.hex())

            messagebox.showinfo("Готово", "Сообщение успешно зашифровано! Чтобы расшифровать, скопируйте и вставьте в поле «Входной текст»")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def decrypt(self):
        """
        Расшифровывает введённый текст.
        Вызывается кнопкой "Расшифровать".
        """
        try:
            key = self.validate_key()
            text = self.validate_input_text()

            # Проверяем, что введён именно hex-текст
            if not is_valid_hex_string(text):
                raise ValueError(
                    "Для расшифрования необходимо ввести зашифрованный текст в hex-формате."
                )

            decrypted = ecb_decrypt(bytes.fromhex(text), key)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, decrypted.decode("utf-8"))

            messagebox.showinfo("Готово", "Сообщение успешно расшифровано")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


    def reset_fields(self):
        """
        Очищает поля и возвращает ключ в исходное состояние.
        """
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.DEFAULT_KEY)

    def exit_app(self):
        """
        Завершает работу программы.
        """
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.root.destroy()

    # ================== СЕРВИС ==================

    def add_copy_paste(self, widget):
        """
        Делает возможным копирование и вставку текста.

        ВАЖНО:
        - Горячие клавиши (Cmd/Ctrl + C/V/X) обрабатываются tkinter автоматически
        - Мы добавляем ТОЛЬКО контекстное меню мыши
        """

        # ===== Контекстное меню мыши =====
        menu = tk.Menu(widget, tearoff=0)

        menu.add_command(
            label="Копировать",
            command=lambda: widget.event_generate("<<Copy>>")
        )
        menu.add_command(
            label="Вставить",
            command=lambda: widget.event_generate("<<Paste>>")
        )
        menu.add_command(
            label="Вырезать",
            command=lambda: widget.event_generate("<<Cut>>")
        )

        # macOS / Windows / Linux (правая кнопка)
        widget.bind("<Button-2>", lambda e: menu.tk_popup(e.x_root, e.y_root))
        widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))


    def center_window(self):
        """
        Размещает окно по центру экрана.
        """
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TeaGUI(root)
    root.mainloop()
