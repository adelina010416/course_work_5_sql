import psycopg2

from constants import params


class DBManager:
    def __init__(self, names):
        # names = {'dbname': dbname, 'areas': name1, 'companies': 'name2', 'vacancies': name2}
        self.dbname = names['dbname']
        self.areas = names['areas']
        self.companies = names['companies']
        self.vacancies = names['vacancies']
        self.conn = psycopg2.connect(dbname=self.dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: db_result (list[tuple])
        """
        self.cur.execute(f"SELECT name, vacancies FROM {self.companies}")
        db_result = self.cur.fetchall()
        return db_result

    def get_all_vacancies(self):
        """
        Получает список с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        :return: db_result (list[tuple])
        """
        self.cur.execute(f"""
        SELECT a.name, a.salary_from, a.salary_to, a.currency, a.url, b.name as company
        FROM {self.vacancies} a
        LEFT JOIN {self.companies} b ON a.company = b.company_id
        """)
        db_result = self.cur.fetchall()
        return db_result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return: int средняя з/п
        """
        self.cur.execute(f"""
        SELECT AVG(salary_from) as avg_salary_from
        FROM {self.vacancies}
        """)
        result = self.cur.fetchall()
        return int(result[0][0])

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: result (list[tuple])
        """
        avg_salary = self.get_avg_salary()
        self.cur.execute(f"SELECT * FROM {self.vacancies} WHERE salary_from > {str(avg_salary)}")
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        :param keyword (str) ключевое слово, по которому нужно осуществлять поиск
        :return: result (list[tuple])
        """
        self.cur.execute(f"SELECT * FROM {self.vacancies} WHERE name LIKE '%{keyword}%'")
        result = self.cur.fetchall()
        return result

    def delete_db(self):
        """Удаляет БД"""
        self.finish()
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute(f'DROP DATABASE {self.dbname}')
            except psycopg2.ProgrammingError:
                print(f'База данных {self.dbname} не найдена.')
        conn.close()

    def finish(self):
        """Прерывает соединение с БД"""
        self.cur.close()
        self.conn.close()
