------------------------------
Настройка меню:
------------------------------

В шаблон через функцию представления отправляется список словарей

```python
menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]
```
в шаблоне перебираем словарь и выводим наименование по ключю
и так же вставляем ссылку.
 
```html
{% for m in menu -%}
    <li><a href="{{m.url}}">{{ m.name }}</a></li>
{% endfor -%}
```

------------------------------
Наследование от base.html
------------------------------
Структура base.html

```html
<!DOCTYPE html>
<html>
<head>
    <link type= "text/css" href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    {% block title -%}

    {% endblock %}
</head>
<body>
    {% block content -%}
        {%- block mainmenu -%}
 
        {% endblock mainmenu -%}
 
    {% endblock %}
</body>
</html>
```

Структура расширяемых шаблонов:

```html
{% extends 'base.html' %}

{% block content %}
{{ super() }}
...
...
...
{% endblock %}
```

------------------------------
Формы в HTML без использования класса Forms
------------------------------------------------------
Функция представления:
```python
@app.route('/contact', methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        print(request.form)
        for i in request.form:
            print(i, "-", request.form[i])
    return render_template('contact.html', menu=menu, title="Обратная связь")
```
Шаблон:

```html
{% extends 'base.html' %}

{% block content %}
{{ super() }}
<form action="/contact" method="post" class="form-contact">
    <p><label>Имя: </label> <input type="text" name="username" value="" required />
    <p><label>Email: </label> <input type="text" name="email" value="" required />
    <p><label>Сообщение: </label>

    <p><textarea name="message" rows="7" cols="40"> </textarea>
    <p><input type="submit" value="Отправить" />
</form>
{% endblock %}
```
При вводе данных данные сохраняются в request.form в виде списка словарей:

    ImmutableMultiDict([('username', 'sdbv'), ('email', 'fbdfb'), ('message', ' dfndfn')])

и их можно перебирать:

    username - sdbv
    email - fbdfb
    message -  dfndfn

или обращаться по ключу:
    
    print(request.form['username'])
    >>> svsdv

Названия ключей соответствуют значению name в шаблоне

    name="username"
    name="email"
    name="message"

    <p><label>Имя: </label> <input type="text" name="username" value="" required />
    <p><label>Email: </label> <input type="text" name="email" value="" required />
    <p><textarea name="message" rows="7" cols="40"> </textarea>



----------------------------
FLASH-сообщения
----------------------------
Это сообщения, которые возвращаются из сессии, которая возникает при отправке информации из формы

```python
from flask import flash

```

В фукнции обработчике, которая принимает POST запрос добавляем

```python
if len(request.form['username']) > 2:
    flash('Сообщение отправлено', category="success")
else:
    flash('Ошибка отправки', category="error")
```
В шаблоне нужно сделать цикл, который будет перебирать значения переменной

```html
{% for cat, msg in get_flashed_message(True) %}
<div class="flash {{cat}}"> {{ msg }}</div>
{% endfor %}
```
Получается, что flash будет содеражть условие, и категорию, которая отображает
режим, либо ошибка, либо успешно
в шаблоне режим выводится в класс объетка div, и если ошибка, то срабатывает один
css, если все в порядке, то другой css

```css
.flash.success {
         border: 1px solid #21DB56;
         background: #AEFFC5;
}
.flash.error {
         border: 1px solid #FF4343;
         background: #FF9C9C;
}
```



