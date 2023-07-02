import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import csv
import os
from matplotlib import patheffects


def create_ndvi_plot(filename):
    # Чтение данных из CSV файла
    dates = []  # Список дат
    values = []  # Список значений NDVI
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            date = datetime.datetime.strptime(
                row[0], "%Y-%m-%d"
            )  # Преобразуем строку даты в объект datetime
            dates.append(date)
            values.append(float(row[1]))

    # Создание графика
    plt.plot(
        dates,
        values,
        "-",
        color="darkblue",
        marker="o",
        markersize=4,
        label="Measurement",
    )  # Точки на кривой обозначены символом "o"

    plt.xlabel("Month")
    plt.ylabel("NDVI value")
    plt.title(
        os.path.splitext(os.path.basename(filename))[0]
    )  # Использование названия файла без расширения
    plt.legend()

    # Добавление сетки из серых линий
    plt.grid(color="gray", linestyle="dotted", alpha=0.25)

    # Форматирование месяцев на оси x
    plt.xticks(rotation=45, ha="right")
    plt.gca().xaxis.set_major_locator(
        mdates.MonthLocator()
    )  # Установка меток месяцев на оси x
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%b %Y")
    )  # Форматирование меток месяцев на оси x
    plt.gca().tick_params(axis="x", which="major", pad=5)  # Сдвиг месяцев на оси x

    # Преобразование дат в числовой формат для точек на графике
    # date_numbers = mdates.date2num(dates)

    # # Добавление дат под осью x
    # for i in range(len(dates)):
    #     plt.text(
    #         date_numbers[i],
    #         min(values) - 0.06 * (max(values) - min(values)),  # Позиция даты под осью x
    #         dates[i].strftime("%d-%m-%Y"),  # Формат даты
    #         ha="center",
    #         va="top",
    #         fontsize=9,
    #         rotation=75,
    #         path_effects=[patheffects.withStroke(linewidth=2, foreground="white")],
    #     )

    # Изменение размера графика
    fig = plt.gcf()
    fig.set_size_inches(21, 9)  # Изменение размера графика (ширина, высота)

    # Установка фиксированного диапазона значений по вертикальной оси
    plt.ylim(-0.2, 1)

    # Сохранение графика в файл
    basename = os.path.splitext(os.path.basename(filename))[0]
    plt.savefig("plots/" + basename + "_plot.png", bbox_inches="tight")
    plt.close()


# Создание папки plots, если она еще не существует
if not os.path.exists("plots"):
    os.makedirs("plots")

# Список файлов для построения кривых
# create_ndvi_plot("data.csv")

# Список файлов для построения кривых
create_ndvi_plot(
    r"C:\Users\nvmax\Desktop\Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes\csv\204030_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv"
)
create_ndvi_plot(
    r"C:\Users\nvmax\Desktop\Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes\csv\204032_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv"
)
create_ndvi_plot(
    r"C:\Users\nvmax\Desktop\Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes\csv\205992_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv"
)
