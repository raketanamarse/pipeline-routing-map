import csv

# Список для хранения точек
data_points = []

# Функция для добавления точки
def add_marker(latitude, longitude, color, marker_number, description, label):
    data_points.append({
        "Широта": latitude,
        "Долгота": longitude,
        "Цвет": color,
        "Номер метки": marker_number,
        "Описание": description,
        "Подпись": label
    })

# Функция для экспорта в CSV
def export_to_csv(file_name):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Широта", "Долгота", "Описание", "Подпись", "Номер метки", "Цвет"])
        writer.writeheader()
        for point in data_points:
            writer.writerow({
                "Широта": point["Широта"],
                "Долгота": point["Долгота"],
                "Описание": point["Описание"],
                "Подпись": point["Подпись"],
                "Номер метки": point["Номер метки"],
                "Цвет": point["Цвет"]
            })

# Пример использования
add_marker(55.7558, 37.6173, "желтый", 1, "Красная площадь, Москва", "Москва")
add_marker(59.9343, 30.3351, "синий", 2, "Дворцовая площадь, Санкт-Петербург", "СПб")

export_to_csv("markers_for_yandex.csv")
