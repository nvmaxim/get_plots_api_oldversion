import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import csv
import os
import numpy as np
from scipy.interpolate import CubicSpline


def create_ndvi_plot(filename, ref_filename):
    # Чтение данных из CSV файла для основного графика
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

    # Чтение данных из CSV файла для reference plot
    ref_dates = []  # Список дат для reference plot
    ref_values = []  # Список значений NDVI для reference plot
    with open(ref_filename, "r") as ref_csvfile:
        ref_reader = csv.reader(ref_csvfile)
        next(ref_reader)  # Пропускаем заголовок
        for row in ref_reader:
            ref_date = datetime.datetime.strptime(
                row[0], "%Y-%m-%d"
            )  # Преобразуем строку даты в объект datetime
            ref_dates.append(ref_date)
            ref_values.append(float(row[1]))

    # Преобразование дат в числовой формат
    dates_num = mdates.date2num(dates)
    ref_dates_num = mdates.date2num(ref_dates)

    # Создание сплайн-интерполянта
    spline_interp = CubicSpline(dates_num, values)
    spline_dates = pd.date_range(min(dates), max(dates), freq="D")
    spline_dates_num = mdates.date2num(spline_dates)
    spline_values = spline_interp(spline_dates_num)

    # Создание сплайн-интерполянта для reference plot
    spline_interp_ref = CubicSpline(ref_dates_num, ref_values)
    spline_dates_ref = pd.date_range(min(ref_dates), max(ref_dates), freq="D")
    spline_dates_ref_num = mdates.date2num(spline_dates_ref)
    spline_values_ref = spline_interp_ref(spline_dates_ref_num)

    # Изменение частоты генерации новых дат
    # spline_dates = pd.date_range(min(dates), max(dates), freq="D")  # Ежедневно
    # spline_dates = pd.date_range(min(dates), max(dates), freq="H")  # Ежечасно
    # spline_dates = pd.date_range(min(dates), max(dates), freq="Min")  # Ежеминутно
    # spline_dates = pd.date_range(min(dates), max(dates), freq="W")  # Еженедельно
    # spline_dates = pd.date_range(min(dates), max(dates), freq="M")  # Ежемесячно
    # spline_dates = pd.date_range(min(dates), max(dates), freq="A")  # Ежегодно

    # Создание графиков без точек
    plt.plot(
        spline_dates,
        spline_values,
        "-",
        color="darkblue",
        label="Measurement",
        alpha=1,
    )  # График без точек

    plt.plot(
        spline_dates_ref,
        spline_values_ref,
        "--",
        color="darkgreen",
        label="Reference",
        alpha=0.35,
    )  # График reference без точек

    # Расчет корреляции
    correlation = np.corrcoef(spline_values, spline_values_ref)[0, 1]

    # Вывод значения корреляции
    plt.text(
        0.5,
        0.9,
        f"Correlation: {correlation:.2f}",
        ha="center",
        va="center",
        transform=plt.gca().transAxes,
    )

    # Корреляция от 0.7 до 1.0 обычно считается очень сильной.
    # Корреляция от 0.4 до 0.7 обычно считается умеренной или средней.
    # Корреляция от 0.2 до 0.4 обычно считается слабой.
    # Корреляция менее 0.2 обычно считается очень слабой или отсутствующей.

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

    # Округление значения корреляции до 2 знаков после запятой
    correlation_rounded = round(correlation, 2)

    # Сохранение графика в файл
    basename = os.path.splitext(os.path.basename(filename))[0]
    plt.savefig(
        "plots_correlation/"
        + basename
        + f"_plot_correlation_{correlation_rounded}.png",
        bbox_inches="tight",
    )
    plt.close()


# Создание папки plots, если она еще не существует
if not os.path.exists("plots_correlation"):
    os.makedirs("plots_correlation")


# Список файлов для построения кривых
# create_ndvi_plot("data1.csv", "data2.csv")

create_ndvi_plot(
    r"C:\Users\nvmax\Desktop\Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes\csv\204030_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv",
    # Путь к CSV файлу для reference plot
    r"C:\Users\nvmax\Desktop\code\get_plots_api\reference\204030_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv",
)
create_ndvi_plot(
    r"C:\Users\nvmax\Desktop\Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes\csv\204032_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv",
    # Путь к CSV файлу для reference plot
    r"C:\Users\nvmax\Desktop\code\get_plots_api\reference\204030_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv",
)
create_ndvi_plot(
    r"C:\Users\nvmax\Desktop\Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes\csv\205992_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv",
    # Путь к CSV файлу для reference plot
    r"C:\Users\nvmax\Desktop\code\get_plots_api\reference\204030_measurement_Kannauj_Kharif2022_GTP_Maize_ClassCloud_SRC_NoDes.csv",
)
