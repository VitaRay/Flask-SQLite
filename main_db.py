# from flask import Flask, render_template
import sqlite3

# app = Flask(__name__)

# @app.route("/")
# def main_page():
#     return render_template('index.html')


cnnct = sqlite3.connect('my_database.db')
c = cnnct.cursor()
user_request = int(input('Подключено успешно. Введите номер одного из запросов:\n1 - Вывести все данные из базы пользователей"\n2 - Изменить данные о пользователе\n3 - Добавить нового пользователя\n4 - Удалить данные пользователя из базы\n5 - Проверить данные пользователя\n6 - Выбрать столбец со всеми username\n'))

if user_request == 1:
    c.execute('SELECT * FROM Users')
    users = c.fetchall()
    for user in users:
        print(user)
elif user_request == 2:
    choose_user = input("Введите имя пользователя\n")
    choose_email = input("Введите новый email\n")
    c.execute('UPDATE Users SET email = ? WHERE username = ?', (choose_email, choose_user))
    choose_age = int(input("Введите новый возраст\n"))
    c.execute('UPDATE Users SET age = ? WHERE username = ?', (choose_age, choose_user))
    print('Данные изменены')
elif user_request == 3:
    choose_user = input("Введите имя нового пользователя\n")
    choose_email = input("Введите email\n")
    choose_age = int(input("Введите возраст\n"))
    c.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', (choose_user, choose_email, choose_age))
    print('Пользователь добавлен')
elif user_request == 4:
    choose_user = input("Введите имя пользователя\n")
    c.execute('DELETE FROM Users WHERE username = ?', (choose_user,))
    print('Пользователь удалён')
elif user_request == 5:
    choose_user = input("Данные какого пользователя вы хотите проверить?\n")
    c.execute("SELECT * FROM Users WHERE username = ?", (choose_user,))
    row = c.fetchone()
    if not row:
        print("Ошибка: имя не найдено!")
    else:
        print(row)
elif user_request == 6:
    pass

else:
    print('Номер указан неверно')

# if __name__ == "main":
#     app.run()

cnnct.commit()
cnnct.close()