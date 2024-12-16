#!/bin/python3

import tkinter as tk
from tkinter import ttk, filedialog
import webbrowser 
from PIL import Image, ImageTk, ImageSequence


#------------------------------------------------------------------------------------------------------------------  
# calculate    
global section_info, coord_dict

import pandas as pd
import os
import gpxpy.gpx
from fastkml import kml
from geopy.distance import geodesic


def calculate():
    # Пути к файлам из глобальных переменных
    print(selected_file1.get()) 
    print(selected_file2.get())

    # Пути к вашим Excel-файлам
    main_file_path = selected_file1.get()
    coord_file_path = selected_file2.get()

    # Читаем данные из основного файла
    main_data = pd.read_excel(main_file_path)

    # Получаем необходимые столбцы
    section_numbers = main_data['Номер секции'].values
    section_lengths = main_data['Длина секции'].values
    wall_thickness = main_data['Средняя толщина стенки, мм'].values
    weld_angle = main_data['Примыкание шва, град'].values

    # Создаем список словарей с данными о каждой секции
    section_info = []
    for num, length, thickness, angle in zip(section_numbers, section_lengths, wall_thickness, weld_angle):
        color = '008000'
        description = f"Средняя толщина стенки, мм {thickness} и Примыкание шва, град {angle}"
        section_info.append({
            'Номер секции': num,
            'Длина секции': length,
            'Широта': None,
            'Долгота': None,
            'Описание': description,
            'Цвет': color
        })

    print(f"Список секций успешно сохранен")

    # Определяем расширение файла
    file_extension = os.path.splitext(coord_file_path)[-1].lower()
    coord_dict = []

    if file_extension == '.xlsx':
        coord_data = pd.read_excel(coord_file_path)
        coordinates = coord_data[['Широта', 'Долгота']].values
        coord_dict = [{'Широта': lat, 'Долгота': lon} for lat, lon in coordinates]
    elif file_extension == '.kml':
        with open(coord_file_path, 'rb') as kml_file:
            kml_data = kml_file.read()
            k = kml.KML()
            k.from_string(kml_data)
            for feature in k.features():
                for placemark in feature.features():
                    if hasattr(placemark, 'geometry') and placemark.geometry:
                        for coord in placemark.geometry.coords:
                            coord_dict.append({'Широта': coord[1], 'Долгота': coord[0]})
    elif file_extension == '.gpx':
        with open(coord_file_path, 'r', encoding='utf-8') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        coord_dict.append({'Широта': point.latitude, 'Долгота': point.longitude})
    else:
        raise ValueError("Неподдерживаемый формат файла")

    return section_info, coord_dict


        










# Функция для расчета расстояния по geopy (более точная версия)
def geopy_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


# Функция для расчета новых координат вдоль вектора с использованием geopy
def calculate_next_point(lat1, lon1, lat2, lon2, distance):
    total_distance = geopy_distance(lat1, lon1, lat2, lon2)

    if total_distance == 0:
        return lat1, lon1  # Если расстояние 0, возвращаем начальную точку

    # Ограничиваем пропорцию значением от 0 до 1
    ratio = min(max(distance / total_distance, 0), 1)

    # Считаем новые координаты
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    new_lat = lat1 + ratio * dlat
    new_lon = lon1 + ratio * dlon

    return new_lat, new_lon


# Функция для обновления координат секций вдоль векторов
def update_section_coordinates(section_info, coord_dict):
    # Устанавливаем первую точку в section_info
    if section_info and coord_dict:
        section_info[0]['Широта'] = coord_dict[0]['Широта']
        section_info[0]['Долгота'] = coord_dict[0]['Долгота']

    # Сначала строим векторы
    vectors = []
    for i in range(len(coord_dict) - 1):
        start_lat = coord_dict[i]['Широта']
        start_lon = coord_dict[i]['Долгота']
        end_lat = coord_dict[i + 1]['Широта']
        end_lon = coord_dict[i + 1]['Долгота']

        # Длина вектора (расстояние между точками)
        vector_distance = geopy_distance(start_lat, start_lon, end_lat, end_lon)
        vectors.append({
            'start_lat': start_lat,
            'start_lon': start_lon,
            'end_lat': end_lat,
            'end_lon': end_lon,
            'distance': vector_distance
        })

    # Начинаем с первой точки из coord_dict
    current_lat = coord_dict[0]['Широта']
    current_lon = coord_dict[0]['Долгота']
    section_index = 1  # Секция уже инициализирована выше
    current_distance = 0.0  # Текущая длина пройденного расстояния

    for i in range(len(vectors)):
        vector = vectors[i]
        start_lat = vector['start_lat']
        start_lon = vector['start_lon']
        end_lat = vector['end_lat']
        end_lon = vector['end_lon']
        vector_length = vector['distance']

        # Пока есть секции, которые нужно обновить
        while section_index < len(section_info) and current_distance < vector_length:
            section = section_info[section_index]
            section_length_km = section['Длина секции'] / 1000  # Длина секции в километрах

            # Если текущая секция вмещается в оставшееся расстояние вектора
            if current_distance + section_length_km <= vector_length:
                # Рассчитываем координаты для этой секции
                next_lat, next_lon = calculate_next_point(start_lat, start_lon, end_lat, end_lon,
                                                          current_distance + section_length_km)
                section['Широта'] = next_lat
                section['Долгота'] = next_lon
                current_distance += section_length_km
                section_index += 1
            else:
                # Если длина секции превышает оставшееся расстояние, идем к следующему вектору
                remaining_distance = vector_length - current_distance
                next_lat, next_lon = calculate_next_point(start_lat, start_lon, end_lat, end_lon,
                                                          current_distance + remaining_distance)
                section['Широта'] = next_lat
                section['Долгота'] = next_lon
                current_distance = vector_length
                break

        # Если текущий вектор исчерпан, но есть еще секции, переходим к следующему вектору
        if current_distance >= vector_length:
            current_distance = 0.0  # Сбрасываем расстояние для следующего вектора

    # Если векторы закончились, а секции еще остались, продолжаем двигаться по направлению последнего вектора
    if section_index < len(section_info):
        # Получаем последние две точки для продолжения направления
        last_vector = vectors[-1]
        start_lat = last_vector['end_lat']
        start_lon = last_vector['end_lon']
        direction_lat = last_vector['end_lat'] - last_vector['start_lat']
        direction_lon = last_vector['end_lon'] - last_vector['start_lon']

        # Расставляем оставшиеся точки вдоль этого направления
        while section_index < len(section_info):
            section = section_info[section_index]
            section_length_km = section['Длина секции'] / 1000  # Длина секции в километрах
            next_lat = start_lat + direction_lat * section_length_km / geopy_distance(start_lat, start_lon,
                                                                                      start_lat + direction_lat,
                                                                                      start_lon + direction_lon)
            next_lon = start_lon + direction_lon * section_length_km / geopy_distance(start_lat, start_lon,
                                                                                      start_lat + direction_lat,
                                                                                      start_lon + direction_lon)

            section['Широта'] = next_lat
            section['Долгота'] = next_lon
            section['Цвет'] = 'FFFF00'  # Желтый цвет для продолжения
            start_lat, start_lon = next_lat, next_lon
            section_index += 1

    return section_info





def calculate_main(section_info, coord_dict):
    # Обновляем координаты для секций
    updated_section_info = update_section_coordinates(section_info, coord_dict)

    # Выводим результат
    for section in updated_section_info:
        print(f"Номер секции: {section['Номер секции']}, "
              f"Длина секции: {section['Длина секции']}, "
              f"Широта: {section['Широта']}, "
              f"Долгота: {section['Долгота']}, "
              f"Цвет: {section['Цвет']}")
        

    import xml.etree.ElementTree as ET

    # Создаем корневой элемент KML
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")

    # Создаем элемент <Document> внутри корня
    document = ET.SubElement(kml, 'Document')

    # Для каждой секции в section_info  добавляем точку
    for section in section_info:
        num = section['Номер секции']  # Извлекаем номер секции
        coords = section  # Все данные о секции

        # Создаем элемент <Placemark> для каждой секции
        placemark = ET.SubElement(document, 'Placemark')

        # Добавляем название секции
        name = ET.SubElement(placemark, 'name')
        name.text = f"С_{num}"

        # Добавляем описание секции с дополнительной информацией
        description = ET.SubElement(placemark, 'description')
        description.text = (f"Номер секции: {coords['Номер секции']}\n"
                            f"Длина секции: {coords['Длина секции']}\n"
                            f"Широта: {coords['Широта']}\n"
                            f"Долгота: {coords['Долгота']}\n"
                            f"Описание: {coords['Описание']}\n"
                            # f"Подпись: {coords['Подпись']}\n"
    )

        # Добавляем координаты <Point>
        point = ET.SubElement(placemark, 'Point')
        coordinates = ET.SubElement(point, 'coordinates')
        coordinates.text = f"{coords['Долгота']},{coords['Широта']},0"  # Формат: долгота,широта,высота (высота = 0)

        # Опционально, можно добавить стиль с цветом метки (если требуется)
        style = ET.SubElement(placemark, 'Style')
        icon_style = ET.SubElement(style, 'IconStyle')
        color = ET.SubElement(icon_style, 'color')
        color.text = coords['Цвет']  # Используем цвет, который хранится в словаре

    # Создаем дерево и записываем его в файл
    tree = ET.ElementTree(kml)
    tree.write('sections.kml', encoding='utf-8', xml_declaration=True)

    print("Файл KML успешно создан.")









#------------------------------------------------------------------------------------------------------------------  
# crypt        

import os
from tkinter import Tk, filedialog, simpledialog, messagebox
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """Генерация ключа на основе пароля и соли"""
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, password: str, output_path: str):
    """Шифрование файла"""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        data = f.read()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_path, 'wb') as f:
        f.write(salt + iv + encrypted_data)

    messagebox.showinfo("Успех", f"Файл успешно зашифрован и сохранён как {output_path}")

def main_crypt():
    root = Tk()
    root.withdraw()

    file_path = "sections.kml"

    password = simpledialog.askstring("Пароль", "Введите пароль для шифрования", show="*")
    if not password:
        messagebox.showerror("Ошибка", "Пароль не может быть пустым")
        return

    output_path = filedialog.asksaveasfilename(title="Сохранить зашифрованный файл", defaultextension=".bin")
    if not output_path:
        return

    try:
        encrypt_file(file_path, password, output_path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось зашифровать файл: {e}")


#------------------------------------------------------------------------------------------------------------------  
# UI      



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
    print("Кнопка СГЕНЕРИРОВАТЬ нажата")
    url = "https://nakarte.me/#m=4/63.80189/101.25000&l=O"
    webbrowser.open(url)


def select_type():
    print("Нажата кнопка сгенерировать KML")
    
    # Вызываем calculate и получаем значения
    section_info, coord_dict = calculate()
    
    # Передаем полученные значения в calculate_main
    calculate_main(section_info, coord_dict)

    main_crypt()



# def select_file(label, success_icon, file_types):
#     file_path = filedialog.askopenfilename(filetypes=file_types)
#     if file_path:
#         success_icon.pack(side=tk.RIGHT, padx=10)
#     else:
#         success_icon.pack_forget()

def select_file(label, success_icon, file_types, file_var):
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        file_var.set(file_path)  # Сохраняем путь в переданную переменную
        success_icon.pack(side=tk.RIGHT, padx=10)
    else:
        file_var.set("")  # Очищаем переменную, если файл не выбран
        success_icon.pack_forget()



def create_success_icon(frame):
    # Создание зеленой галочки
    check_image = Image.open("check_icon.png").resize((20, 20))  # Убедитесь, что у вас есть "check_icon.png"
    check_icon = ImageTk.PhotoImage(check_image)
    success_label = tk.Label(frame, image=check_icon, background="#f0f0f0")
    success_label.image = check_icon
    return success_label


def main():
    

    root = tk.Tk()
    root.title("Пример интерфейса")
    root.geometry("600x400")
    root.configure(bg="#f0f0f0")

    global selected_file1, selected_file2  # Сделайте переменные глобальными
    selected_file1 = tk.StringVar()
    selected_file2 = tk.StringVar()


    style = ttk.Style()
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 11, "bold"), foreground="#333333")

    frame = ttk.Frame(root, padding="20 20 20 20")
    frame.pack(expand=True, fill=tk.BOTH)

    title_label = ttk.Label(frame, text="Вычисление координат секций трубопровода", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=(0, 20))

    # Первый файл
    file_frame1 = ttk.Frame(frame)
    file_frame1.pack(pady=5, fill=tk.X)

    label1 = ttk.Label(file_frame1, text="Выбрать файл с базой данных")
    label1.pack(side=tk.LEFT)

    success_icon1 = create_success_icon(file_frame1)

    selected_file1 = tk.StringVar()

    btn1 = ttk.Button(
        file_frame1,
        text="Выбрать файл Excel",
        command=lambda: select_file(label1, success_icon1, [("Excel файлы", "*.xls *.xlsx")], selected_file1)
    )
    btn1.pack(side=tk.LEFT, padx=10)

    # Второй файл
    file_frame2 = ttk.Frame(frame)
    file_frame2.pack(pady=5, fill=tk.X)

    label2 = ttk.Label(file_frame2, text="Выбрать файл с известными координатами")
    label2.pack(side=tk.LEFT)

    success_icon2 = create_success_icon(file_frame2)

    selected_file2 = tk.StringVar()

    btn2 = ttk.Button(
        file_frame2,
        text="Выбрать файл Excel",
        command=lambda: select_file(label2, success_icon2, [("Excel файлы", "*.xls *.xlsx")], selected_file2)
    )
    btn2.pack(side=tk.LEFT, padx=10)

    # Нижние кнопки
    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(pady=10)

    btn_action2 = ttk.Button(buttons_frame, text="Справка",  command=action_2)
    btn_action2.grid(row=0, column=0, padx=5)

    btn_action3 = ttk.Button(buttons_frame, text="Сгенерировать", command=action_3)
    btn_action3.grid(row=0, column=1, padx=5)

    # Экспорт
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    export_frame = ttk.Frame(bottom_frame)
    export_frame.pack()

    export_label = ttk.Label(export_frame, text="Экспортировать как:")
    export_label.grid(row=0, column=0, padx=5)

    type_button = ttk.Button(export_frame, text="KML", command=select_type)
    type_button.grid(row=0, column=1, padx=5)

    # Центрирование
    export_frame.grid_columnconfigure(0, weight=1)
    export_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
