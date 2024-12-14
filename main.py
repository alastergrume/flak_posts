import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from FDataBase import FDataBase

# Conf DATABASE
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'f1site.db')))

# Перебираем список и по каждому ключу подставляем имя и url
menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


def connect_db():
    """Функция для связи с БД"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    """Используется переменная g, которая создается в контектсе приложения"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    """Используется переменная g, которая создается в контексте приложения
        Соединение разрывается при уничтожении контекста, когда сессия разрывается"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def print_hi():
    db = get_db()  # Соединяемся с БД
    dbase = FDataBase(db)
    return render_template("index.html", menu=dbase.getMenu(), post=dbase.getPostsAnonce())

@app.route('/add_post', methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")

@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)



#
#
# @app.route('/about')
# def about():
#     return render_template("about.html", menu=menu, title='О сайте')
#
#
# @app.route("/profile/<username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#
#     return f"Пользователь: {username}"
#
#
# @app.route('/contact', methods=["GET", "POST"])
# def contacts():
#     if request.method == "POST":
#         # Для отображения flash сообщения
#         if len(request.form['username']) > 2:
#             flash("Сообщение отправлено", category='success')
#         else:
#             flash("Ошибка отправки", category='error')
#     return render_template('contact.html', menu=menu, title="Обратная связь")
#
#
# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     if request.method == "POST":
#         if request.form['username'] == "ivan" and request.form['psw'] == "123":
#             session['userLogged'] = request.form['username']
#             return redirect(url_for('profile', username=session['userLogged']))
#     return render_template('login.html', title="Авторизация", menu=menu)
#
#
# @app.route('/delete-visits/')
# def delete_visits():
#     """
#     Для удаления сессии
#     """
#     session.pop('userLogged', None)  # удаление данных о посещениях
#     return 'Visits deleted' "Total visits: {}".format(session.get('userLogged'))
#

@app.errorhandler(404)
def pageNotFound(error):
    """
    Возвращает страницу "Страница не найдена"
    """
    db = get_db()
    dbase = FDataBase(db)
    return render_template('page404.html', title='Страница не найдена', menu=dbase.getMenu())


if __name__ == '__main__':
    app.run(debug=True)
    create_db()
