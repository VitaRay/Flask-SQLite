from flask import Flask, request
import sqlite3

#Функция выбора всех заметок из БД
def selectAllNotesFunc():
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    #Присваиваем переменной notes выборку всех элементов из таблицы list_of_notes
    notes = c.execute("SELECT * FROM list_of_notes").fetchall()
    #Сохраняем данные и закрываем соединение
    cnnct.commit()
    cnnct.close()
    #возвращаем выборку
    return notes


#Функция добавления новой заметки
def AddNewNoteFunc():
    #Присваиваем переменной title ответ из формы с заголовком
    title = request.form['title']
    #Присваиваем переменной description ответ из формы с описанием
    description = request.form["description"]
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    #Добавляем в БД заголовок и описание
    inserting = c.execute("INSERT Into list_of_notes (title, content) VALUES (?, ?)", (title, description))
    #Сохраняем данные и закрываем соединение
    cnnct.commit()
    cnnct.close()
    #Возращаем функцию вставки
    return inserting


#Функция редактирования заметки
def editNoteFunc(noteId):
    #Присваиваем переменной title ответ из формы с заголовком
    title = request.form['title']
    #Присваиваем переменной description ответ из формы с описанием
    description = request.form["description"]
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    #Обновляем данные в таблице
    updating = c.execute('UPDATE list_of_notes SET title = ? WHERE id = ?', (title, noteId))
    updating = c.execute('UPDATE list_of_notes SET content = ? WHERE id = ?', (description, noteId))
    #Сохраняем данные и закрываем соединение
    cnnct.commit()
    cnnct.close()
    #Возращаем функцию обновления данных
    return updating


#Функция регистрации
def registerFunc():
    #Присваиваем переменной userLogin ответ из формы с логином
    userLogin = request.form['userLogin']
    #Присваиваем переменной userEmail ответ из формы с почтой
    userEmail = request.form['userEmail']
    #Присваиваем переменной userPassword ответ из формы с паролем 
    userPassword = request.form['userPassword']
    #Присваиваем переменной checkUserPassword ответ из формы с проверкой пароля 
    checkUserPassword = request.form['checkUserPassword']
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    #Выбираем имя пользователя если оно есть в БД, которое он ввёл 
    findUserLogin = c.execute("SELECT login FROM user_account_table WHERE login = ?", (userLogin,)).fetchone()
    #Выбираем почту пользователя, если она есть в БД, которую он ввёл
    findUserEmail = c.execute("SELECT email FROM user_account_table WHERE email = ?", (userEmail,)).fetchone()
    #Сохраняем данные и закрываем соединение
    cnnct.commit()
    cnnct.close()
    #Проверяем: если в БД есть такая же запись логина, то возвращяем ошибку 
    if findUserLogin != None:
        return 'loginErrorResponse'
    #Проверяем: если в БД есть такая же запись почты, то возвращаем ошибку
    elif findUserEmail != None:
        return 'emailErrorResponse'
    #Проверяем: если пароли, которые ввел пользователь не совпадают, то их записывать нельзя и выводится ошибка
    elif userPassword != checkUserPassword:
        return 'passwordErrorResponse'
    #В остальных случаях возвращается успешный ответ
    else:
        return 'seccessRegister'
    

def loginFunc():
    #Присваиваем переменной userLogin ответ из формы с логином
    userLogin = request.form['userLogin']
    #Присваиваем переменной userPassword ответ из формы с паролем 
    userPassword = request.form['userPassword']
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    findUserLogin = c.execute("SELECT login FROM user_account_table WHERE login = ?", (userLogin,)).fetchone()
    findUserPassword = c.execute('SELECT password FROM user_account_table WHERE password = ?', (userPassword,)).fetchone()
    if (findUserLogin == None) or (findUserPassword == None):
        return 'login Or Password Error'
    else:
        return 'success Login'     