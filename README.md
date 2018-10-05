# Recycled-cars
Приложение имеет несколько функций:
1. Добавить автомобиль в БД.
2. Получить список автомобилей, которые были в строю в указанный период времени. 
________________________________________________________________________________

Для запуска приложения необходимо:
1) Изменить параметры подключения к БД (180 строка):
con = psycopg2.connect(database="DB_test", user="postgres", password="*********", host="127.0.0.1",
                           port="5432")
________________________________________________________________________________
Для "main.py" - в день утилизации автомобиль считается в строю.
Для "main2.py" - в день утилизации автомобиль не считается в строю.
