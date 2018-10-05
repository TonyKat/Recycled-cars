import re
import os
import io
import sys
import psycopg2
from datetime import datetime
from PIL import Image


def input_data(regex, text, current_position):
    matches = re.findall(regex, input(text))
    while not matches:
        try:
            print('Некорректные данные!')
            matches = re.findall(regex, input(text))
        except:
            print('Некорректные данные!')
    if (current_position == '1' and matches[0] == '0') or (current_position == '2' and matches[0] == '0'):
        sys.exit()
    return matches[0]


def input_path():
    while True:
        absolute_path = input('Введите абсолютный путь к скану PTS в формате jpeg: ')
        if absolute_path == '0':
            break
        try:
            if os.path.exists(absolute_path) is True:
                with open(absolute_path, 'rb') as image:
                    img = image.read()
                break
            else:
                print('Файл не найден!')
                continue
        except:
            print('Ошибка поиска файла!')

    if absolute_path == '0':
        sys.exit()
    else:
        return img, absolute_path


def input_date(text):
    while True:
        try:
            str_dt = input(text + '(формат YYYY/MM/DD): ')
            if str_dt == '0':
                break
            dt = datetime.strptime(str_dt, '%Y/%m/%d')
            break
        except:
            print('Некорректные данные!')
            continue
    if str_dt == '0':
        sys.exit()
    else:
        return dt


def print_list(loc_rows):
    num = 0
    current_row = 0
    while num < len(loc_rows):
        print('\n{}. VIN - {}. \nДата выпуска - {}.\nДата утилизации - {}.'
              .format(num + 1, loc_rows[num][0], loc_rows[num][2], loc_rows[num][3]))

        num += 1
        current_row += 1

        if current_row == 10:
            current_row = 0
            command = input_data(r"^[0123]{1}$", '\nПродолжить вывод следующих 10 записей, нажмите - "1".'
                                                 '\nВернуться к предудущим 10 записям, нажмите - "2".'
                                                 '\nЗакончить вывод, нажмите - "3".\nВведите: ', "2")
            if command == '1':
                continue
            elif command == '2':
                if num == 10:
                    print('\nВыведены первые 10 записей, предыдущих 10 записей пока не существует.')
                    command2 = input_data(r"^[012]{1}$", '\nПродолжить вывод следующих 10 записей, нажмите - "1".'
                                                         '\nЗакончить вывод, нажмите - "2".\nВведите: ', "2")
                    if command2 == '1':
                        continue
                    elif command2 == '2':
                        break
                    else:
                        print('\nПереход в главное меню...')
                        sys.exit()

                else:
                    num -= 20
                    continue
            elif command == '3':
                break

    return


def main_menu():
    try:

        print('\nГлавное меню:'
              '\n1. Добавить новое авто, нажмите - "1".'
              '\n2. Получить список не утилизированных авто в указанный период, нажмите - "2".'
              '\n3. Выход из приложения, нажмите - "0".'
              '\n---------------------------------------------------------'
              '\n(Для отмены действий в пунктах "1" или "2" - нажмите "0".)\n')
        number = input_data("^[012]{1}$", 'Введите: ', '0')

        if number == '1':
            vin = input_data("^[0]$|^[0123456789ABCDEFGHJKLMNPRSTUVWXYZ]{17}$", 'Введите VIN: ', number)
            pts_b, path_image = input_path()

            while True:
                date_begin = input_date('Введите дату выпуска ')
                date_end = input_date('Введите дату утилизации ')
                if date_begin > date_end:
                    print('\nДата утилизации не может быть раньше даты выпуска!\n')
                    continue
                else:
                    break

            cur.execute('INSERT INTO public."Recycled_cars" (vin, pts, begin_date, end_date)'
                        ' VALUES (%s, %s, %s, %s)', (vin, pts_b, date_begin, date_end))
            con.commit()
            print('\nАвтомобиль успешно добавлен в базу данных!')
            return '1'

        elif number == '2':
            while True:
                begin_interval = input_date('Введите дату начала периода ')
                end_interval = input_date('Введите дату окончания периода ')
                if begin_interval > end_interval:
                    print('\nДата начала периода не может быть раньше даты окончания периода!\n')
                    continue
                else:
                    break
            cur.execute('SELECT vin, pts, begin_date, end_date FROM public."Recycled_cars" '
                        'WHERE (%s between begin_date and end_date) or '
                        '(%s between begin_date and end_date) or '
                        '(begin_date between %s and %s);',
                        (begin_interval, end_interval, begin_interval, end_interval))
            rows = cur.fetchall()
            print('\nВыводится список автомобилей бывших в строю в указанный период.\n'
                  '-----------------------------------------------------------------\n'
                  '(В день утилизации автомобиль считается в строю.)')
            print_list(rows)
            if len(rows) != 0:
                input_data("^[01]{1}$", '\nДля просмотра скана PTS - нажмите "1",'
                                        ' а затем введите номер автомобиля в выведенном списке: ', number)
                while True:
                    try:
                        regex = str("^[0-9]" + "{1," + str(len(str(rows.index(rows[-1])))) + "}" + "$")
                        loc_number = input_data(regex, 'Номер автомобиля: ', '22')
                        if loc_number == '0':
                            break
                        image = Image.open(io.BytesIO(rows[int(loc_number) - 1][1]))
                        image.show()
                        image.close()
                        continue
                    except:
                        print('Не удалось открыть скан или такого такого номера не существует.')
                return '2'
            else:
                print('Подходящих авто не найдено.')

        elif number == '0':
            print('\nДо свидания!')
            return '0'
        else:
            print('\nМожно вводить только: "0", "1", "2".')
    except:
        print('\nПереход в главное меню...')


if __name__ == '__main__':
    print('\nДобро пожаловать в приложение "Утилизация автомобилей".')
    con = psycopg2.connect(database="DB_test", user="postgres", password="**********", host="127.0.0.1",
                           port="5432")
    cur = con.cursor()

    cur.execute('select exists(select * from information_schema.tables where table_name=%s)', ('Recycled_cars',))
    if cur.fetchone()[0] == False:
        cur.execute('''CREATE TABLE public."Recycled_cars"
            (
                vin character varying(17),
                pts bytea,
                begin_date date,
                end_date date,
                PRIMARY KEY (vin)
            )
            WITH (
                OIDS = FALSE
            )
            TABLESPACE pg_default;

            ALTER TABLE public."Recycled_cars"
                OWNER to postgres;''')
        con.commit()

    while True:
        main_number = main_menu()
        if main_number == '0':
            con.close()
            break
    exit()
