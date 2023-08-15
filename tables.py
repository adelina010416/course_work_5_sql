import psycopg2

from constants import params
from hh_api import APIhh


def get_company_id(company_names: list, db_name: str):
    """
    Возвращает список id запрашиваемых компаний.
    :param company_names: (list) список названий компаний
    :param db_name: (str) название БД
    :return: result (list) список id
    """
    result = []
    conn = psycopg2.connect(dbname=db_name, **params)
    try:
        with conn:
            with conn.cursor() as cur:
                for name in company_names:
                    cur.execute(f"SELECT * FROM employers WHERE company_name LIKE '%{name}%'")
                    company = cur.fetchall()
                    if company:
                        result.append(*company)
    finally:
        conn.close()
    return result


def insert_data(data: list, names: dict):
    """
    Заполняет данными таблицы БД.
    :param data: (list) список названий компаний
    :param names: (dict) словарь с названиями БД и таблиц
    """
    # names = {'dbname': dbname, 'areas': name1, 'companies': 'name2', 'vacancies': name2}
    ids = []
    companies = get_company_id(data, names['dbname'])
    [ids.append(comp[0]) for comp in companies]
    user_data = APIhh.get_user_data(ids)
    conn = psycopg2.connect(dbname=names['dbname'], **params)
    conn.autocommit = True
    cur = conn.cursor()
    while True:
        try:
            for area in user_data['areas']:
                try:
                    cur.execute(f"INSERT INTO {names['areas']} (area_id, name) VALUES (%s, %s)",
                                (area['id'], area['name']))
                except Exception as e:
                    print(e)
            for company in user_data['companies']:
                try:
                    cur.execute(f"INSERT INTO {names['companies']} (company_id, name, description, site, hh_url, area, "
                                f"vacancies) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (company['id'], company['name'], company['description'], company['site_url'],
                                 company['alternate_url'], company['area']['id'], company['open_vacancies']))
                except Exception as e:
                    print(e)
                    continue
            for vacancy in user_data['vacancies']:
                try:
                    cur.execute(f"INSERT INTO {names['vacancies']} (vacancy_id, name, area, salary_from, salary_to, "
                                f"currency, address, url, company) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (vacancy['id'], vacancy['name'], vacancy['area']['id'], vacancy['salary']['from'],
                                 vacancy['salary']['to'], vacancy['salary']['currency'], vacancy['address']['raw'],
                                 vacancy['alternate_url'], vacancy['employer']['id']))
                except Exception as e:
                    print(e)
                    continue
            break
        except psycopg2.ProgrammingError:
            create_tables(names)
    conn.commit()
    conn.close()


def create_tables(names: dict):
    """
    Создаёт 3 связанных между собой таблицы: с компаниями, вакансиями и регионами.
    :param names: (dict) {'dbname': dbname, 'areas': name1, 'companies': 'name2', 'vacancies': name2}
    """
    conn = psycopg2.connect(dbname=names['dbname'], **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"CREATE TABLE {names['areas']} ("
                    "area_id INTEGER PRIMARY KEY,"
                    "name VARCHAR(50))")
        cur.execute(f"CREATE TABLE {names['companies']} ("
                    "company_id INTEGER PRIMARY KEY,"
                    "name VARCHAR(60),"
                    "description TEXT,"
                    "site VARCHAR(100),"
                    "hh_url VARCHAR(100),"
                    f"area INTEGER REFERENCES {names['areas']}(area_id),"
                    "vacancies INTEGER)")
        cur.execute(f"CREATE TABLE {names['vacancies']} ("
                    "vacancy_id INTEGER PRIMARY KEY,"
                    "name VARCHAR(100),"
                    f"area INTEGER REFERENCES {names['areas']}(area_id),"
                    "salary_from INTEGER,"
                    "salary_to INTEGER,"
                    "currency VARCHAR(6),"
                    "address VARCHAR(60),"
                    "url VARCHAR(100),"
                    f"company INTEGER REFERENCES {names['companies']}(company_id))")
    conn.close()
