import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def filter_log_file():
    # Запрашиваем имя файла без расширения
    filename_without_extension = input("Введите имя файла без расширения (например, 'my_log'): ")
    log_filename = filename_without_extension + '.log'
    txt_filename = filename_without_extension + '.txt'

    try:
        # Открываем файл .log для чтения с разными кодировками
        try:
            with open(log_filename, 'r', encoding='utf-8') as log_file:
                lines = log_file.readlines()
        except UnicodeDecodeError:
            # Если возникает ошибка декодирования, пробуем другую кодировку
            with open(log_filename, 'r', encoding='latin-1') as log_file:
                lines = log_file.readlines()

        # Фильтруем строки, содержащие 'In :1401FA92'
        filtered_lines = [line for line in lines if 'In :1401FA92' in line]

        # Записываем отфильтрованные строки в новый файл .txt
        with open(txt_filename, 'w', encoding='utf-8') as txt_file:
            txt_file.writelines(filtered_lines)

        print(f"Фильтрация завершена. Результат записан в файл: {txt_filename}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {log_filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    log_filename = txt_filename  # filename_without_extension + '.txt'
    output_filename = 'out.txt'

    try:
        # Открываем файл .txt для чтения
        with open(log_filename, 'r', encoding='utf-8') as log_file:
            lines = log_file.readlines()

        # Инициализируем список для записи результатов
        output_lines = []

        # Проходим по строкам с шагом 2
        for i in range(0, len(lines), 2):
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip() if i + 1 < len(lines) else ''

            # Извлекаем нужные части строк
            if 'In :1401FA92[07]00' in line1:
                output_lines.append(line1)  # Добавляем перевод строки
            if 'In :1401FA92[07]01' in line2:
                # Извлекаем 4 символа после 'In :1401FA92[07]01'
                additional_part = line2[32:36]  # 32 - это индекс первого символа после 'In :1401FA92[07]01'
                if additional_part:
                    output_lines[-1] += additional_part + '\n'  # Добавляем к последней строке и перевод строки

        # Записываем результаты в файл out.txt
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.writelines(output_lines)

        print(f"Обработка завершена. Результат записан в файл: {output_filename}")

    except FileNotFoundError:
        print(f"Ошибка: Файл {log_filename} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Функция для чтения данных из файла
def read_data(file_name):
    times = []
    params1 = []
    params2 = []
    params3 = []
    params4 = []

    with open(file_name, 'r') as file:
        for line in file:
            # Разделяем строку на время и параметры
            parts = line.split(' ', 1)
            if len(parts) < 2:
                continue  # Пропускаем строки с недостаточным количеством данных

            time_str, data_hex = parts
            time = datetime.strptime(time_str, "%H:%M:%S.%f")

            # Проверяем, что строка data_hex достаточно длинная
            if len(data_hex) < 36:  # 48:
                print(f"Недостаточно данных в строке: {line.strip()}")
                continue

            # Извлекаем параметры из строки формата HEX
            param1 = int(data_hex[21:23], 16)
            param2 = int(data_hex[25:27], 16)
            param3 = int(data_hex[29:31], 16)
            param4 = int(data_hex[33:35], 16)

            # Добавляем данные в соответствующие списки
            times.append(time)
            params1.append(param1)
            params2.append(param2)
            params3.append(param3)
            params4.append(param4)

    return times, params1, params2, params3, params4


# Функция для построения графика
def plot_data(times, params1, params2, params3, params4):
    plt.figure(figsize=(10, 6))

    # Настройка формата времени на оси X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    # Построение графиков для каждого параметра
    plt.plot(times, params1, label='Адрес извещателя', marker='o')
    plt.plot(times, params2, label='Обработанное значение', marker='o')
    plt.plot(times, params3, label='Необработанное значение дыма', marker='o')
    plt.plot(times, params4, label='Необработанное значение температуры', marker='o')

    # Добавление заголовков и меток
    plt.title('Зависимость параметров от времени')
    plt.xlabel('Время')
    plt.ylabel('Значение параметров')
    plt.legend()
    plt.grid()

    # Поворот меток на оси X для лучшей читаемости
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Показ графика
    plt.show()


# Основная часть программы
if __name__ == "__main__":
    # Запускаем функцию фильтрации и объединения строк данных
    filter_log_file()
    file_name = 'out.txt'
    times, params1, params2, params3, params4 = read_data(file_name)
    plot_data(times, params1, params2, params3, params4)
