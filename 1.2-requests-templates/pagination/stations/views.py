import csv
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    stations = []

    try:
        with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as csvfile:
            # Читаем все строки
            lines = csvfile.readlines()

            # Пропускаем вторую строку (русские заголовки)
            # Оставляем только первую строку (английские заголовки) и данные
            filtered_lines = [lines[0]] + lines[2:]

            # Создаем reader из отфильтрованных строк
            reader = csv.DictReader(filtered_lines, delimiter=';')

            for row in reader:
                # Используем английские названия колонок
                name = row.get('Name', '')
                street = row.get('PlaceDescription', '')
                district = row.get('District', '')

                # Очищаем кавычки
                name = name.strip('"') if name else ''
                street = street.strip('"') if street else ''
                district = district.strip('"') if district else ''

                if name:
                    stations.append({
                        'Name': name,
                        'Street': street,
                        'District': district
                    })

    except FileNotFoundError:
        stations = [
            {'Name': 'Файл не найден', 'Street': '', 'District': ''},
        ]
    except Exception as e:
        stations = [
            {'Name': f'Ошибка: {str(e)}', 'Street': '', 'District': ''},
        ]

    # Пагинация - 10 элементов на страницу
    paginator = Paginator(stations, 10)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page не integer, показываем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # Если page вне диапазона, показываем последнюю страницу
        page = paginator.page(paginator.num_pages)

    context = {
        'bus_stations': page.object_list,  # список станций на текущей странице
        'page': page,  # объект страницы для пагинации
    }

    return render(request, 'stations/index.html', context)