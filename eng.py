# -*- coding: UTF-8 -*-
import os
from flask import Flask, g, render_template, request, jsonify, url_for, send_file, redirect
from models import db_session, User,Dish,Category,Restaurant,Reservation
import settings
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import uuid
from datetime import datetime

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = str(uuid.uuid4())
manager = LoginManager(app)
#Определяем маршрут по которому будет проходить авторизация
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':#Проверяем что получили запрос на принятие данных
        username = request.form['name']
        password = request.form['password']#получаем данные имя пользователя и пароль, если все сходится логиним пользователя
        user = User.query.filter_by(name=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('Main', page_name='index'))
        else:
            # В случае неверного логина или пароля, вы можете вернуть ошибку или перенаправить обратно на страницу входа
            return render_template('login', error='Invalid username or password')
    return render_template("login.htm")
#Разавторизуемся из пользователя
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('Main', page_name='index'))
@app.route("/")
def index():
    return redirect(url_for("Main"))

from datetime import datetime

from datetime import datetime

@app.route("/reservations")
def reservations():
    # Получаем все резервирования из базы данных
    reservations = db_session.query(Reservation).all()
    # Передаем данные о резервированиях в HTML-шаблон
    return render_template("reservations.html", reservations=reservations)
@app.route("/reservation/", methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        fio = request.form['fio']
        phone = request.form['phone']
        guests_count = int(request.form['guests_count'])
        datetime_str = request.form['datetime']

            # Преобразование строкового значения в datetime объект
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        new_reservation = Reservation(FIO=fio, phone=phone, guests_count=guests_count, datetime=datetime_obj)
        db_session.add(new_reservation)
        db_session.commit()

    # Получение всех бронирований для отображения в календаре
    reservations = db_session.query(Reservation).all()
    event_days = {}
    for reservation in reservations:
        date_str = reservation.datetime.strftime('%Y-%m-%d')
        if date_str not in event_days:
            event_days[date_str] = 'available'
        event_days[date_str] = 'booked'

    return render_template("reservation.htm", event_days=event_days)



#Загружаем пользователя
@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
#Регистрируем пользователя после получения запроса post когда принимаем данные на сервер, работает по аналогии с авторизацией
#Только без проверки корректности введенных данных
@app.route("/registration/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        new_user = User(name=username, password=password, mail=email)
        db_session.add(new_user)
        db_session.commit()
        login_user(new_user)
        return redirect(url_for('Main'))
    return render_template("registration.htm")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404

@app.route('/Contacts/')
def Contacts():
    restaurant = db_session.query(Restaurant).first()
    return render_template('Contacts.htm',Rest=restaurant)
@app.route('/aboutUs/')
def about_us():
    restaurant = db_session.query(Restaurant).first()
    return render_template('AboutUs.htm',Rest=restaurant)
#Обработчик главной страницы, получаем из бд все категории товаров и сами товары
@app.route("/dish/")
def Main():
    categories = db_session.query(Category).all()
    products = db_session.query(Dish).all()
    return render_template('dish.htm', page_name='Товары', categories=categories, product=products)

#Обработчик страницы с товарами для мужчин
@app.route("/men/")
def men():
    categories = db_session.query(Category).all()
    products = db_session.query(Dish).all()
    return render_template("reservation.htm", page_name="men", categories=categories, product=products, is_male=True)

#Обработчик заказов пользователя, показывает все заказы, которые были совершены пользователем


#Обработчик страницы с корзиной товаров, где получаем все товары из корзины текущего пользователя,и считаем общую сумму его заказа


#Получаем товар по его id, используем в основном для просмотра подробной карточки о товаре
@app.route("/dish/dish_info/<int:id>/")
def dish_by_id(id):
    item = db_session.query(Dish).filter(Dish.id == id).first()
    return render_template("dish_info.htm", card_item=item)
#Такой же обработчик, только для категорий, пользователь выбрал категорию, и теперь на странице только товары категории с id выбранной
@app.route("/dish/<int:category_id>/")
def dish_by_category(category_id):
    item = db_session.query(Dish).filter(Dish.category_id == category_id).all()
    categories = db_session.query(Category).all()
    return render_template("dish_category.htm", page_name="tovar", product=item,category=categories)
#Аналогичный обработчик
@app.route("/Category/<int:category_id>/")
def chooseCategory(category_id):
    # Получаем продукты определенной категории из базы данных
    products = db_session.query(Dish).filter(Dish.category_id == category_id).all()
    category_ = db_session.query(Category).all()
    return render_template("Category.htm", Category=category_, products=products, is_male=False)



@app.route("/<page_name>/")
def dish(page_name):
    return render_template(page_name + ".htm")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5057, debug=True)
