from pprint import pprint

import databases
import tables
from db_manager import DBManager
from validators import validate_table_name, validate_companies


def get_settings():
    """
    Запрашивает название базы данных, с которой хочет работать пользователь
    Создаёт словарь формата {'dbname': dbname, 'areas': areas, 'companies': companies, 'vacancies': vacancies}
    :return:
    db_settings (dict): название базы данных и названия таблиц
    """
    user_db = input('Пожалуйста, введите название уже существующей или новой БД, с которой хотите работать.\n')
    setting_db_name, tables_exist = databases.create_db(user_db)
    companies = input('Введите названия таблиц, с которыми хотите работать:\n'
                      '* название талицы с компаниями: ')
    areas = input('* название таблицы с регионами: ')
    vacancies = input('* название таблицы с вакансиями: ')
    db_settings = validate_table_name(setting_db_name,
                                      {'areas': areas, 'companies': companies, 'vacancies': vacancies})
    db_settings['dbname'] = setting_db_name
    print(f'Текущие настройки: {db_settings}')
    return db_settings


def get_query():
    """
    Определяет запрос пользователя и вызывает соответствующие функции (главное меню приложения).
    Возможные команды: companies (ввод названий компаний, данные которых нужно сохранить в БД);
                       settings (изменить название БД, с которой вы хотите работать);
                       bd_work (перейти в режим работы с БД);
                       exit (завершить работу программы)
    """
    print('Добро пожаловать!')
    db_settings = get_settings()
    print('\nВозможные команды:\n* companies - ввод названий компаний, данные которых вы хотите сохранить в БД\n'
          '* settings - изменить название БД, с которой вы хотите работать\n'
          '* db_work - перейти в режим работы с БД\n'
          '* exit - завершить работу программы')
    while True:
        user_query = input('Введите команду: ').lower()
        if user_query == 'companies':
            companies = validate_companies()
            tables.insert_data(companies, db_settings)
            print('Готово! Данные внесены в БД.')
        elif user_query == 'settings':
            db_settings = get_settings()
            print('Настройки сохранены.')
        elif user_query == 'db_work':
            print('\nВы вошли в режим работы с БД. Возможные команды:\n'
                  '* vacs_count - вывод списка всех компаний и количества вакансий у каждой компании\n'
                  '* vacs_info - вывод списка всех вакансий с указанием названия компании, зарплаты '
                  'и ссылки на вакансию\n'
                  '* avg_salary - вывод средней зарплаты по всем вакансиям\n'
                  '* higher_salary - вывод списка всех вакансий, у которых зарплата выше средней\n'
                  '* search - поиск вакансий в БД по ключевому слову\n'
                  '* delete - удаление БД\n'
                  '* exit - выход из режима работы с БД\n')
            new_settings = db_work(db_settings)
            if new_settings:
                db_settings = new_settings
        elif user_query == 'exit':
            break
        else:
            print("Команда не распознана. Пожалуйста, повторите запрос.")


def db_work(settings):
    """
    Меню работы с базой данных.
    Возможные команды: vacs_count - вывод списка всех компаний и количества вакансий у каждой компании
                       vacs_info - вывод списка всех вакансий с указанием названия компании, зарплаты, и ссылки
                       avg_salary - вывод средней зарплаты по всем вакансиям
                       higher_salary - вывод списка всех вакансий, у которых зарплата выше средней
                       search - поиск вакансий в БД по ключевому слову
                       delete - удаление БД
                       exit - выход из режима работы с БД
    :param settings: (dict) название базы данных и названия таблиц.
    :return: new_settings (dict) при удалении БД запрашивает названия новой БД и таблиц
    """
    db = DBManager(settings)
    new_settings = None
    while True:
        query = input('Введите команду: ').lower()
        if query == 'vacs_count':
            pprint(db.get_companies_and_vacancies_count())
        elif query == 'vacs_info':
            pprint(db.get_all_vacancies())
        elif query == 'avg_salary':
            print(db.get_avg_salary())
        elif query == 'higher_salary':
            pprint(db.get_vacancies_with_higher_salary())
        elif query == 'search':
            keyword = input('Введите слово для поиска: ')
            pprint(db.get_vacancies_with_keyword(keyword))
        elif query == 'delete':
            db.delete_db()
            print(f'БД {settings["dbname"]} удалена. Чтобы продолжить, задайте новые настройки.')
            new_settings = get_settings()
        elif query == 'exit':
            db.finish()
            print('Выход в главное меню.')
            return new_settings
        else:
            print("Команда не распознана. Пожалуйста, повторите запрос.")


if __name__ == '__main__':
    get_query()
