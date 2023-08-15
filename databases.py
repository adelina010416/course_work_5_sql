import psycopg2

from constants import params
from hh_api import APIhh
from validators import validate_query


def update(db_name):
    """
    Обновляет данные таблицы employers (список компаний и их id)
    :param db_name: (str) имя БД
    """
    employers = APIhh.get_all_employers()
    conn = psycopg2.connect(dbname=db_name, **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL
                )
            """)
        for employer in employers:
            try:
                cur.execute("INSERT INTO employers (employer_id, company_name) VALUES (%s, %s)",
                            (employer['id'], employer['name']))
            except psycopg2.IntegrityError:
                continue
    conn.commit()
    conn.close()


def create_db(db_name):
    """
    Создаёт новую БД или обновляет уже существующую.
    :param db_name: (str) имя БД
    :return: db_name: (str) имя БД
             tables_exist: list[tuple] список существующих в БД таблиц
    """
    tables_exist = []
    while True:
        try:
            connection = psycopg2.connect(dbname='postgres', **params)
            cur = connection.cursor()
            connection.autocommit = True
            cur.execute(f"CREATE DATABASE {db_name}")
            connection.close()
            update(db_name)

        except psycopg2.ProgrammingError:
            decision = validate_query(db_name)

            if decision.lower() == 'create':
                db_name = input('Выберете другое имя для новой БД.\n')

            elif decision.lower() == 'update':
                conn1 = psycopg2.connect(dbname=db_name, **params)
                with conn1.cursor() as cur1:
                    cur1.execute(f"DROP TABLE employers")
                    cur1.execute("""SELECT table_name FROM information_schema.tables
                                    WHERE table_schema = 'public'""")
                    tables_exist = cur1.fetchall()
                conn1.commit()
                conn1.close()
                update(db_name)
                break

        else:
            break

    return db_name, tables_exist
