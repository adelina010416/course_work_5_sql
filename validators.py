import psycopg2

import tables
from constants import params


def validate_query(db_name):
    """
    Проверяет запрос клиента. Возможные варианты: create (создать БД), update (обновить данные БД).
    :param db_name: (str) имя БД
    :return: decision (str) запрос пользователя
    """
    while True:
        decision = input(f'База данных с именем {db_name} уже существует. '
                         f'Хотите обновить БД {db_name} или создать новую?\n'
                         f'(Введите "create" или "update")\n')
        if decision in ['create', 'update']:
            return decision
        print('Неверный запрос. Пожалуйста, введите "create" или "update".')


def validate_table_name(db_name: str, user_table_names: dict):
    """
    Проверяет, что пользователь ввёл имена трёх существующих в БД связанных между собой таблиц
    или имена трёх новых таблиц.
    :param db_name: (str) имя БД
    :param user_table_names: (dict) словарь с именами таблиц
    :return: user_table_names: (dict) словарь с именами таблиц
    """
    db_table_names_str = ''
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT table_name FROM information_schema.tables
                            WHERE table_schema = 'public'""")
            db_table_names = cur.fetchall()
    for name in db_table_names:
        db_table_names_str += f'{str(name)}, '
    conn.close()
    while True:
        result = []
        for name in user_table_names.values():
            if (name,) not in db_table_names:
                result.append('False')
        if 'False' not in result:
            user_table_names['dbname'] = db_name
            return user_table_names
        if ' '.join(result).count('False') == 3:
            user_table_names['dbname'] = db_name
            tables.create_tables(user_table_names)
            return user_table_names
        print(f'Введены некорректные данные.\n'
              f'Пожалуйста, введите названия трёх связанных существующих таблиц или '
              f'трёх новых.\nСейчас в БД есть таблицы: {db_table_names_str[:-2]}')
        user_table_names['companies'] = input('* название талицы с компаниями: ')
        user_table_names['areas'] = input('* название таблицы с регионами: ')
        user_table_names['vacancies'] = input('* название таблицы с вакансиями: ')


def validate_companies():
    """
    Проверяет, корректен ли пользовательский ввод компаний.
    :return: companies (list) список компаний
    """
    while True:
        companies = input('\nВведите названия компаний через ", "\n').split(', ')
        [print(comp) for comp in companies]
        user_answer = input('Проверьте, что все названия введены верно.\n'
                            'Если допущена ошибка, введите "no", иначе - "yes": ')
        if user_answer.lower() == 'yes':
            return companies
