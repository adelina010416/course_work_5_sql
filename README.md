# Проект по работе с БД
***
## Краткое описание
Проект позволяет получать данные о компаниях и вакансиях с сайта hh.ru,
проектировать таблицы в БД PostgreSQL и загружать полученные данные в созданные таблицы.
## Список возможных команд
* **companies** - ввод названий компаний, данные которых нужно сохранить в БД
* **settings** - изменить название БД, с которой вы хотите работать
* **bd_work** - перейти в режим работы с БД
  * *vacs_count* - вывод списка всех компаний и количества вакансий у каждой компании
  * *vacs_info* - вывод списка всех вакансий с указанием названия компании, зарплаты, и ссылки
  * *avg_salary* - вывод средней зарплаты по всем вакансиям
  * *higher_salary* - вывод списка всех вакансий, у которых зарплата выше средней
  * *search* - поиск вакансий в БД по ключевому слову
  * *delete* - удаление БД
  * *exit* - выход из режима работы с файлом
* **exit** - завершить работу программы
