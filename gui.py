"""
GUI для алгоритма TEA
Автор: студент Лукьянов Александр Дмитриевич

Этот файл отвечает за графический интерфейс программы.
Здесь создаётся окно, кнопки и поля ввода.

Сам алгоритм шифрования находится в файле tea.py.
"""
# Графический интерфейс пользователя для алгоритма TEA
# Инициализация главного окна приложения

# Подключаем библиотеку tkinter — она нужна для создания окон
import tkinter as tk

# ttk — более современный и аккуратный вид кнопок и надписей
# messagebox — всплывающие окна с сообщениями
from tkinter import ttk, messagebox

# Импортируем функции шифрования и расшифрования из tea.py
from tea import ecb_encrypt, ecb_decrypt


class TeaGUI:
    """
    Класс TeaGUI описывает всё окно программы.
    Можно сказать, что этот класс — это вся программа целиком.
    """

    def __init__(self, root):
        """
        Эта функция вызывается при запуске программы.
        Здесь создаётся окно и все элементы интерфейса.
        """

        # Сохраняем главное окно в переменную
        self.root = root

        # Заголовок окна (отображается сверху)
        self.root.title("TEA by Александр Лукьянов")

        # Размер окна: ширина x высота
        self.root.geometry("420x560")

        # Запрещаем изменять размер окна мышью
        self.root.resizable(False, False)

        # Размещаем окно по центру экрана
        self.center_window()

        # ===== ОСНОВНОЙ КОНТЕЙНЕР =====
        # Это как большая коробка, куда кладутся все элементы интерфейса
        container = ttk.Frame(root, padding=20)
        container.pack(expand=True)

        # Заголовок внутри окна
        ttk.Label(
            container,
            text="TEA by Александр Лукьянов",
            font=("Helvetica", 18, "bold")
        ).pack(pady=10)

        # Подсказка пользователю
        ttk.Label(
            container,
            text="Введите данные для шифрования",
            foreground="gray"
        ).pack(pady=5)

        # ===== ПОЛЕ ДЛЯ КЛЮЧА =====

        # Надпись над полем ключа
        ttk.Label(container, text="Ключ (hex):").pack(anchor="w", pady=(20, 5))

        # Поле, куда пользователь вводит ключ
        self.key_entry = ttk.Entry(container, width=40)
        self.key_entry.pack()

        # Сразу вставляем пример ключа
        self.key_entry.insert(0, "00112233445566778899aabbccddeeff")

        # ===== ПОЛЕ ДЛЯ ВХОДНОГО ТЕКСТА =====

        # Надпись над полем текста
        ttk.Label(container, text="Входной текст:").pack(anchor="w", pady=(15, 5))

        # Большое поле для ввода текста
        self.input_text = tk.Text(container, height=6, width=40)
        self.input_text.pack()

        # ===== КНОПКИ УПРАВЛЕНИЯ =====

        # Отдельный блок для кнопок
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=20)

        # Кнопка "Зашифровать"
        ttk.Button(
            button_frame,
            text="Зашифровать",
            command=self.encrypt
        ).grid(row=0, column=0, padx=5)

        # Кнопка "Расшифровать"
        ttk.Button(
            button_frame,
            text="Расшифровать",
            command=self.decrypt
        ).grid(row=0, column=1, padx=5)

        # Кнопка "Сбросить"
        ttk.Button(
            button_frame,
            text="Сбросить",
            command=self.reset_fields
        ).grid(row=0, column=2, padx=5)

        # ===== ПОЛЕ ДЛЯ РЕЗУЛЬТАТА =====

        # Надпись над результатом
        ttk.Label(container, text="Результат:").pack(anchor="w", pady=(10, 5))

        # Поле, где отображается результат
        self.output_text = tk.Text(container, height=6, width=40)
        self.output_text.pack()

        # ===== КНОПКА ВЫХОДА =====
        ttk.Button(
            container,
            text="Выйти",
            command=self.exit_app
        ).pack(pady=15)

        # ===== КОПИРОВАНИЕ И ВСТАВКА =====
        # Добавляем поддержку горячих клавиш и мыши
        self.add_copy_paste(self.key_entry)
        self.add_copy_paste(self.input_text)
        self.add_copy_paste(self.output_text)

        # Если пользователь нажимает на крестик окна — тоже выходим корректно
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def add_copy_paste(self, widget):
        """
        Делает возможным копирование и вставку текста.

        Работает:
        - Command+C / V / X — на macOS
        - Ctrl+C / V / X — на Windows и Linux
        - Правый клик мыши — на всех системах
        """

        # ===== macOS =====
        widget.bind("<Command-c>", lambda e: widget.event_generate("<<Copy>>"))
        widget.bind("<Command-v>", lambda e: widget.event_generate("<<Paste>>"))
        widget.bind("<Command-x>", lambda e: widget.event_generate("<<Cut>>"))

        # ===== Windows / Linux =====
        widget.bind("<Control-c>", lambda e: widget.event_generate("<<Copy>>"))
        widget.bind("<Control-v>", lambda e: widget.event_generate("<<Paste>>"))
        widget.bind("<Control-x>", lambda e: widget.event_generate("<<Cut>>"))

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

        # Правый клик мыши
        widget.bind("<Button-2>", lambda e: menu.tk_popup(e.x_root, e.y_root))
        widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    def center_window(self):
        """
        Размещает окно ровно по центру экрана.
        """
        self.root.update_idletasks()

        w = self.root.winfo_width()      # ширина окна
        h = self.root.winfo_height()     # высота окна

        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)

        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def encrypt(self):
        """
        Шифрует введённый текст.
        Вызывается кнопкой "Зашифровать".
        """
        try:
            # Получаем ключ из поля
            key = bytes.fromhex(self.key_entry.get().strip())

            # Получаем текст пользователя
            text = self.input_text.get("1.0", tk.END).strip()

            # Шифруем текст
            encrypted = ecb_encrypt(text.encode("utf-8"), key)

            # Очищаем поле результата
            self.output_text.delete("1.0", tk.END)

            # Показываем зашифрованный текст
            self.output_text.insert(tk.END, encrypted.hex())

            # Сообщаем, что всё прошло успешно
            messagebox.showinfo("Готово", "Сообщение успешно зашифровано")

        except Exception as e:
            # Если произошла ошибка — показываем сообщение
            messagebox.showerror("Ошибка", str(e))

    def decrypt(self):
        """
        Расшифровывает введённый текст.
        Вызывается кнопкой "Расшифровать".
        """
        try:
            key = bytes.fromhex(self.key_entry.get().strip())
            text = self.input_text.get("1.0", tk.END).strip()

            # Расшифровываем текст
            decrypted = ecb_decrypt(bytes.fromhex(text), key)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, decrypted.decode("utf-8"))

            messagebox.showinfo("Готово", "Сообщение успешно расшифровано")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def reset_fields(self):
        """
        Очищает поля ввода и результата.
        """
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)

    def exit_app(self):
        """
        Завершает работу программы.
        Перед выходом спрашивает подтверждение.
        """
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.root.destroy()


# ===== ТОЧКА ВХОДА В ПРОГРАММУ =====
# Этот код выполняется при запуске файла
if __name__ == "__main__":
    root = tk.Tk()          # создаём окно
    app = TeaGUI(root)      # создаём интерфейс
    root.mainloop()         # запускаем программу

