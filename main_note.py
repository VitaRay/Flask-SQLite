from flask import Flask, render_template, request, redirect, url_for
import my_funcs as db_funcs
import sqlite3


#Создание объекта "__name__" и присваивание ему переменной
app = Flask(__name__)
    

#Задание маршрута главной страницы со списком заметок
@app.route("/")
def mainPageFunc():
    return render_template('index.html', notes = db_funcs.selectAllNotesFunc())


@app.route("/note/<noteId>")
def CurrentNotePageFunc(noteId):
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    c.execute("SELECT * FROM list_of_notes WHERE id = ?", (noteId))
    note = c.fetchone()
    #Сохраняем данные и закрываем соединение
    cnnct.commit()
    cnnct.close()
    return render_template("note.html", note = note, noteId = noteId)


#Задание маршрута страницы с формой добавления заметок
@app.route("/add-note", methods=["GET", "POST"])
def CheckRequestMethodNewNoteFunc():
    #Если на странице с формой метод GET: возвращаем страницу с формой 
    if request.method == "GET":
        return render_template("add_note.html")
    #Если на странице с формой метод POST:
    else:
        #Вызываем функцию добавления заметки
        db_funcs.AddNewNoteFunc()
        #Пересылаем на страницу, которая указана в функции notes
        return redirect(url_for("mainPageFunc"))


@app.route('/removing-note/<noteId>')
def removeNoteFunc(noteId):
    #Подключаемся к БД
    cnnct = sqlite3.connect('notes_database.db')
    #Присваиваем переменной c создание курсора
    c = cnnct.cursor()
    c.execute("DELETE FROM list_of_notes WHERE id = ?", (noteId))
    #Сохраняем данные и закрываем соединение
    cnnct.commit()
    cnnct.close()
    return redirect(url_for("mainPageFunc"))


@app.route('/edit-note/<noteId>', methods=["GET", "POST"])
def CheckRequestMethodEditNoteFunc(noteId):
    #Если на странице с формой метод GET: возвращаем страницу с формой 
    if request.method == "GET":
        return render_template("edit_note.html", noteId = noteId)
    #Если на странице с формой метод POST:
    else:
        #Вызываем функцию добавления заметки
        db_funcs.editNoteFunc(noteId)
        #Пересылаем на страницу, которая указана в функции notes
        return redirect(url_for("mainPageFunc"))



@app.route('/register', methods=['GET', 'POST'])
def CheckRequestMethodRegisterFunc():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        response = db_funcs.registerFunc()
        if response == 'loginErrorResponse':
            return render_template('login_error.html')
        elif response == 'emailErrorResponse':
            return render_template('email_error.html')
        elif response == 'passwordErrorResponse':
            return render_template('password_error.html')
        else:
            return render_template('success_register.html')


@app.route('/password-error')
def passwordErrorPageFunc():
    return render_template('password_error.html')


@app.route('/login-error')
def loginErrorPageFunc():
    return render_template('login_error.html')


@app.route('/email-error')
def emailErrorPageFunc():
    return render_template('email_error.html')


@app.route('/success-register')
def successRegisterPageFunc():
    return render_template('success_register.html')


@app.route('/login', methods=['GET', 'POST'])
def checkRequestMethodLoginFunc():
    if request.method == "GET":
        return render_template('login.html')
    else:
        response = db_funcs.loginFunc()
        return response


#Запуск приложения
if __name__ == '__main__':
    app.run(debug = True)