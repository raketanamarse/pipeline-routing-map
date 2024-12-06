import os
import folium
from xml.dom import minidom
import webbrowser

# Функция для извлечения точек из KML-файла
def extract_points_from_kml(kml_file):
    points = []
    kml_doc = minidom.parse(kml_file)
    placemarks = kml_doc.getElementsByTagName('Placemark')

    for placemark in placemarks:
        coordinates = placemark.getElementsByTagName('coordinates')[0].childNodes[0].data.strip()
        lon, lat, _ = map(float, coordinates.split(','))
        points.append((lat, lon))
    return points

# Функция для отображения карты с точками
def display_map_with_points(kml_file):
    # Извлечение точек из KML файла
    points = extract_points_from_kml(kml_file)
    
    if not points:
        print("Точки не найдены в KML файле.")
        return

    # Создание карты, центрированной на первой точке
    map_center = points[0]
    folium_map = folium.Map(location=map_center, zoom_start=10)

    # Добавление стандартного слоя для карты
    folium.TileLayer('OpenStreetMap').add_to(folium_map)

    # Добавление точек на карту
    for lat, lon in points:
        folium.Marker(location=(lat, lon)).add_to(folium_map)

    # Добавление переключателя между типами карт
    folium.LayerControl().add_to(folium_map)

    # Сохранение карты в файл
    map_file = 'map_with_points.html'
    folium_map.save(map_file)
    print(f"Карта сохранена в файл {map_file}. Открывается в браузере...")

    # Открытие карты в браузере
    webbrowser.open(f"file://{os.path.abspath(map_file)}")

# Пример использования
kml_file = 'sections.kml'  # Укажите путь к вашему KML файлу
display_map_with_points(kml_file)
