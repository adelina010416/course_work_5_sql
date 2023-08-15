SELECT name, vacancies FROM companies;

SELECT a.name, a.salary_from, a.salary_to, a.currency, a.url, b.name as company FROM vacancies a
LEFT JOIN companies b ON a.company = b.company_id;

SELECT AVG(salary_from) as avg_salary_from FROM vacancies;

SELECT * FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies);

SELECT * FROM vacancies WHERE name LIKE '%python%';

DROP DATABASE dbname;

SELECT * FROM employers WHERE company_name LIKE '%name%';

INSERT INTO areas (area_id, name) VALUES (%s, %s);

INSERT INTO companies (company_id, name, description, site, hh_url, area, vacancies)
VALUES (%s, %s, %s, %s, %s, %s, %s);

INSERT INTO vacancies (vacancy_id, name, area, salary_from, salary_to, currency, address, url, company)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);

CREATE TABLE areas (area_id INTEGER PRIMARY KEY, name VARCHAR(50));

CREATE TABLE companies (company_id INTEGER PRIMARY KEY, name VARCHAR(60), description TEXT, site VARCHAR(100),
                        hh_url VARCHAR(100), area INTEGER REFERENCES areas(area_id), vacancies INTEGER);

CREATE TABLE vacancies (vacancy_id INTEGER PRIMARY KEY, name VARCHAR(100), area INTEGER REFERENCES areas(area_id),
                        salary_from INTEGER, salary_to INTEGER, currency VARCHAR(6), address VARCHAR(60),
                        url VARCHAR(100), company INTEGER REFERENCES companies(company_id));

CREATE TABLE employers (employer_id INTEGER PRIMARY KEY, company_name VARCHAR(255) NOT NULL);

INSERT INTO employers (employer_id, company_name) VALUES (%s, %s);

CREATE DATABASE db_name;

DROP TABLE employers;

SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
