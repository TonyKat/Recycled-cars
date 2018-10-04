# Recycled-cars
Приложение имеет несколько функций:
1. Добавить автомобиль в БД.
2. Получить список автомобилей, которые были в строю в указанный период времени. 
________________________________________________________________________________

Для запуска приложения необходимо:
1) изменить параметры подключения к БД:
con = psycopg2.connect(database="DB_test", user="postgres", password="*********", host="127.0.0.1",
                           port="5432")
2) для повторного запуска приложения необходимо закомментировать создания таблицы:
cur.execute('''
    CREATE TABLE public."Recycled_cars"
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
