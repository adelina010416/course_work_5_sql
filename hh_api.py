import requests


class APIhh:
    """Класс для работы с API"""

    @staticmethod
    def get_all_employers():
        """
        Получает данные всех компаний.
        :return: all_companies (list[dict]) список словарей с id и названием компаний
        """
        print('Обновляю данные по компаниям...')
        params = {'per_page': '100',
                  'only_with_vacancies': 'true'}
        all_companies = []
        page = 0
        while True:
            params['page'] = page
            response = requests.get('https://api.hh.ru/employers', params=params)
            try:
                employers = response.json()['items']
            except KeyError:
                return all_companies
            for employer in employers:
                all_companies.append({'id': employer['id'], 'name': employer['name']})
            page += 1

    @staticmethod
    def get_user_data(ids: list):
        """
        Получает данные запрашиваемых компаний.
        :param ids: (list) список id компаний
        :return: (dict) словарь с данными для трёх таблиц (данные компаний, регионов и вакансий)
        """
        user_employers = []
        user_vacancies = []
        user_areas = []
        area_ids = set()

        for cid in ids:
            employer = requests.get(f'https://api.hh.ru/employers/{cid}').json()
            vacancy = requests.get(f'https://api.hh.ru/vacancies?employer_id={cid}').json()['items']
            user_employers.append(employer)
            user_vacancies += APIhh.check_vacancy(vacancy)

            for i in vacancy:
                area_ids.add(i['area']['id'])
            area_ids.add(employer['area']['id'])
        for aid in area_ids:
            area = requests.get(f'https://api.hh.ru/areas/{aid}').json()
            user_areas.append({'id': area['id'], 'name': area['name']})

        return {'areas': user_areas, 'companies': user_employers, 'vacancies': user_vacancies}

    @staticmethod
    def check_vacancy(vacancies):
        """
        Меняет значение адреса и зарплаты под заданный формат.
        :param vacancies: list[dict]
        :return: vacancies list[dict]
        """
        for vacancy in vacancies:
            if not vacancy["address"]:
                vacancy["address"] = {"raw": None}
            if not vacancy['salary']:
                vacancy['salary'] = {'from': None, 'to': None, 'currency': None}
        return vacancies
