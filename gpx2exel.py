import os
import gpxpy
import pandas as pd

# Функция для конвертации GPX в Excel
def gpx_to_excel(gpx_file_path, excel_file_path):
    # Чтение GPX файла
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    # Список для хранения точек
    points = []

    # Извлечение координат точек
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'Широта': point.latitude,
                    'Долгота': point.longitude
                })

    # Создание DataFrame для данных
    df = pd.DataFrame(points)

    # Добавление пустого столбца для номера
    df.insert(0, 'Номер', '')

    # Сохранение в Excel файл
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

# Функция для поиска всех GPX файлов в директории и конвертации их в Excel
def convert_all_gpx_in_directory(directory):
    # Получение списка файлов в директории
    files = os.listdir(directory)

    # Фильтрация файлов с расширением .gpx
    gpx_files = [file for file in files if file.endswith('.gpx')]

    if not gpx_files:
        print("Нет файлов формата GPX в указанной директории.")
        return

    # Конвертация каждого GPX файла в Excel
    for gpx_file in gpx_files:
        gpx_path = os.path.join(directory, gpx_file)
        excel_path = os.path.join(directory, os.path.splitext(gpx_file)[0] + '.xlsx')
        try:
            gpx_to_excel(gpx_path, excel_path)
            print(f"Успешно конвертирован файл: {gpx_file} -> {os.path.basename(excel_path)}")
        except Exception as e:
            print(f"Ошибка при обработке файла {gpx_file}: {e}")

# Пример использования
directory = './'  # Укажите путь к директории с GPX файлами
convert_all_gpx_in_directory(directory)
