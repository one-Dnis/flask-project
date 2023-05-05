import flask_login
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import logout_user, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from cars import app, db
from cars.models import check_email_in_db, Article, User, Car, Order


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('posts'))
        except:
            return "Ошибка при добавлении"
    return render_template('create-article.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('/posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('/post-detail.html', article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('posts'))
    except:
        return 'Ошибка при удалении'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.text = request.form['text']

        try:
            db.session.commit()
            # return redirect(f'/posts/{article.id}')
            return redirect(url_for('post_detail', id=article.id))
        except:
            db.session.rollback()
            return 'Ошибка при попытке обновить данные в статье'
    else:
        return render_template('/post_update.html', article=article)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            if check_email_in_db(email):
                user = User.query.filter_by(email=email.lower()).first()
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash('неверный логин или пароль')

            else:
                flash('неверный логин или пароль')
        else:
            flash('поля не должны быть пустыми')

    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        and_login = request.form.get('and_login')

        if password and email:
            if request.form.get('password') != request.form.get('password2'):
                flash('Пароли не совпали')
                return render_template('registration.html', name=name, email=email)
            elif check_email_in_db(email):
                flash('указанный email уже зарегистрирован')
                return render_template('registration.html', name=name, email=email)

        else:
            flash('заполните email и password')
            return render_template('registration.html', name=name, email=email)

        user = User(name=name, email=email.lower(), password=generate_password_hash(password))

        try:
            db.session.add(user)
            db.session.commit()

            if and_login:
                login_user(user)
                return redirect(url_for('index'))

            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('registration error')
            return render_template('registration.html', name=name, email=email)
    return render_template('registration.html')


@app.route('/add-car', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        model = request.form.get('model')
        color = request.form.get('color')
        number = request.form.get('number')
        price_per_hour = request.form.get('price_per_hour')

        #запилить проверку тут

        car = Car(model=model, color=color, number=number, price_per_hour=price_per_hour)
        try:
            db.session.add(car)
            db.session.commit()

            return redirect(url_for('cars'))
        except:
            db.session.rollback()
            flash('car database error')
            return render_template(
                'add-car.html', model=model, color=color, number=number, price_per_hour=price_per_hour
            )

    return render_template('add-car.html')


@app.route('/cars')
def cars():
    cars_list = Car.query.all()
    return render_template('cars-page.html', cars=cars_list)


@app.route('/cars/<int:id>')
def car_detail(id):
    car = Car.query.get(id)
    return render_template('car-detail.html', car=car)


@app.route('/order/<int:id>', methods=['POST', 'GET'])
def order(id):
    if request.method == 'POST':
        car = Car.query.get(id)
        user_id = flask_login.current_user.id
        car_id = car.id
        #решить вопрос с форматом даты
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        price = request.form.get('price')
        print(start_date)
        print(end_date)
        return render_template('order.html')
    # order = Order(
    #     user_id=user_id, car_id=car_id, start_date=start_date, end_date=end_date, price=price)
    return render_template('order.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # session['username'] = None
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')
