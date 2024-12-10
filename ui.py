#!/bin/python3

import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser 
from PIL import Image, ImageTk, ImageSequence


def select_file(label, filetypes):
    filename = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=filetypes
    )
    if filename:
        label.config(text=filename)


def action_2():
    gif_window = tk.Toplevel()
    gif_window.title("GIF Анимация")

    gif_path = "example.gif"  # Укажите путь к вашему GIF
    gif_image = Image.open(gif_path)

    gif_width, gif_height = gif_image.size
    gif_window.geometry(f"{gif_width}x{gif_height}")
    gif_window.resizable(False, False)

    gif_label = ttk.Label(gif_window)
    gif_label.pack()

    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]
    delay = gif_image.info.get('duration', 100)

    def play_gif(frame=0):
        gif_label.config(image=frames[frame])
        gif_label.image = frames[frame]
        next_frame = (frame + 1) % len(frames)
        gif_window.after(delay, play_gif, next_frame)

    play_gif()


def action_3():
    print("Кнопка 3 нажата")
    url = "https://nakarte.me/#m=4/63.80189/101.25000&l=O"
    webbrowser.open(url)



def select_type():
    print("Нажата кнопка 'Тип'")


def main():
    root = tk.Tk()
    root.title("Пример интерфейса")
    root.geometry("600x400")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 11, "bold"), foreground="#333333")

    frame = ttk.Frame(root, padding="20 20 20 20")
    frame.pack(expand=True, fill=tk.BOTH)

    title_label = ttk.Label(frame, text="Вычисление координат секций трубопровода", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=(0, 20))

    label1 = ttk.Label(frame, text="Выбрать файл с базой данных")
    label1.pack(pady=5)
    btn1 = ttk.Button(
        frame, 
        text="Выбрать файл Excel", 
        command=lambda: select_file(label1, [("Excel файлы", "*.xls *.xlsx")])
    )
    btn1.pack(pady=5)

    label2 = ttk.Label(frame, text="Выбрать файл с известными координатами")
    label2.pack(pady=5)

    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(pady=10)

    btn_action1 = ttk.Button(buttons_frame, 
        text="Выбрать файл Excel", 
        command=lambda: select_file(label2, [("Excel файлы", "*.xls *.xlsx")])
    )
    btn_action1.grid(row=0, column=0, padx=5)

    btn_action2 = ttk.Button(buttons_frame, text="Справка", command=action_2)
    btn_action2.grid(row=0, column=1, padx=5)

    btn_action3 = ttk.Button(buttons_frame, text="Сгенерировать", command=action_3)
    btn_action3.grid(row=0, column=2, padx=5)



    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    export_frame = ttk.Frame(bottom_frame)
    export_frame.pack()

    export_label = ttk.Label(export_frame, text="Экспортировать как:")
    export_label.grid(row=0, column=0, padx=5)

    type_button = ttk.Button(export_frame, text="Тип", command=select_type)
    type_button.grid(row=0, column=2, padx=5)

    # Центрирование внутри export_frame
    export_frame.grid_columnconfigure(0, weight=1)
    export_frame.grid_columnconfigure(1, weight=1)
    export_frame.grid_columnconfigure(2, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()















# import tkinter as tk
# from tkinter import ttk, filedialog
# import webbrowser 
# from PIL import Image, ImageTk, ImageSequence




# def select_file(label, filetypes):
#     filename = filedialog.askopenfilename(
#         title="Выберите файл",
#         filetypes=filetypes
#     )
#     if filename:
#         label.config(text=filename)




# def action_2():
#     # Создаем новое окно
#     gif_window = tk.Toplevel()
#     gif_window.title("GIF Анимация")

#     # Загрузка GIF
#     gif_path = "example.gif"  # Укажите путь к вашему GIF
#     gif_image = Image.open(gif_path)

#     # Получаем размеры GIF
#     gif_width, gif_height = gif_image.size
#     gif_window.geometry(f"{gif_width}x{gif_height}")
#     gif_window.resizable(False, False)

#     # Виджет Label для отображения GIF
#     gif_label = ttk.Label(gif_window)
#     gif_label.pack()

#     # Загрузка кадров GIF
#     frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]
#     delay = gif_image.info.get('duration', 100)  # Задержка между кадрами

#     # Функция для отображения кадров
#     def play_gif(frame=0):
#         gif_label.config(image=frames[frame])
#         gif_label.image = frames[frame]
#         next_frame = (frame + 1) % len(frames)
#         gif_window.after(delay, play_gif, next_frame)

#     # Запуск анимации
#     play_gif()





# def action_3():
#     print("Кнопка 3 нажата")
#     # Открываем веб-страницу
#     url = "https://nakarte.me/#m=4/63.80189/101.25000&l=O"
#     webbrowser.open(url)




# def main():
#     # Создаем главное окно
#     root = tk.Tk()
#     root.title("Пример интерфейса")
#     root.geometry("600x400")  # Задаём побольше размер окна
#     root.configure(bg="#f0f0f0")  # Светлый фон

#     # Создаем стиль для ttk
#     style = ttk.Style()
#     style.configure("TFrame", background="#f0f0f0")
#     style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
#     style.configure("TButton", font=("Helvetica", 11, "bold"), foreground="#333333")

#     # Фрейм для удобства расположения виджетов
#     frame = ttk.Frame(root, padding="20 20 20 20")
#     frame.pack(expand=True, fill=tk.BOTH)

#     # Заголовок приложения
#     title_label = ttk.Label(frame, text="Вычисление координат секций трубопровода", font=("Helvetica", 16, "bold"))
#     title_label.pack(pady=(0, 20))

#     # Первая кнопка и метка (только для Excel)
#     label1 = ttk.Label(frame, text="Выбрать файл с базой данных")
#     label1.pack(pady=5)
#     btn1 = ttk.Button(
#         frame, 
#         text="Выбрать файл Excel", 
#         command=lambda: select_file(label1, [("Excel файлы", "*.xls *.xlsx")])
#     )
#     btn1.pack(pady=5)




#     # Вторая кнопка и метка (без ограничений)
#     label2 = ttk.Label(frame, text="Выбрать файл с известными координатами")
#     label2.pack(pady=5)

#     # Три кнопки в одной строке под label2
#     buttons_frame = ttk.Frame(frame)
#     buttons_frame.pack(pady=10)

#     btn_action1 = ttk.Button(buttons_frame, 
#         text="Выбрать файл Excel", 
#         command=lambda: select_file(label2, [("Excel файлы", "*.xls *.xlsx")])
#     )
#     btn_action1.grid(row=0, column=0, padx=5)

#     btn_action2 = ttk.Button(buttons_frame, text="Справка", command=action_2)
#     btn_action2.grid(row=0, column=1, padx=5)

#     btn_action3 = ttk.Button(buttons_frame, text="Сгенерировать", command=action_3)
#     btn_action3.grid(row=0, column=2, padx=5)

#     root.mainloop()

# if __name__ == "__main__":
#     main()






