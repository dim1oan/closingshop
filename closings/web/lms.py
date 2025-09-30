from flask import Flask, redirect, render_template, request, abort, flash, jsonify, url_for
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms.forms import AddItem, RegisterForm, LoginForm, ChangePassword, ChangeSity, ChangeGender, \
    ChangeProductInterest, BalanceIn, BalanceOut, AddStore
from data import db_session, api
from data.users import User
from data.items import Item
from data.stores import Store
from data.want_buy_item import WantBuyItem
from data.buy_item import BuyItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице."

db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Главная страница
@app.route("/")
def index():
    db_sess = db_session.create_session()
    items = db_sess.query(Item).filter(Item.is_see == True).limit(8).all()

    categories = [
        {'id': 1, 'name': 'Футболки', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 2, 'name': 'Джинсы', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 3, 'name': 'Платья', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 4, 'name': 'Обувь', 'image_url': 'https://via.placeholder.com/300x200'}
    ]

    return render_template("index.html",
                           title='FashionStore - Главная',
                           products=items,
                           categories=categories,
                           current_user=current_user)


# Страница категории
@app.route('/category/<int:category_id>')
def category(category_id):
    db_sess = db_session.create_session()

    category_map = {
        1: 'футболка', 2: 'джинсы', 3: 'платье', 4: 'обувь'
    }

    type_wear = category_map.get(category_id, '')
    items = db_sess.query(Item).filter(
        Item.type_wear.contains(type_wear),
        Item.is_see == True
    ).all()

    category_name = {
        1: 'Футболки', 2: 'Джинсы', 3: 'Платья', 4: 'Обувь'
    }.get(category_id, 'Категория')

    category_obj = {'id': category_id, 'name': category_name}

    categories = [
        {'id': 1, 'name': 'Футболки', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 2, 'name': 'Джинсы', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 3, 'name': 'Пладья', 'image_url': 'https://via.placeholder.com/300x200'},
        {'id': 4, 'name': 'Обувь', 'image_url': 'https://via.placeholder.com/300x200'}
    ]

    return render_template("category.html",
                           title=f'{category_name} - FashionStore',
                           products=items,
                           category=category_obj,
                           categories=categories,
                           current_user=current_user)


# Страница товара
@app.route('/product/<int:product_id>')
def product(product_id):
    db_sess = db_session.create_session()
    product = db_sess.query(Item).filter(Item.id == product_id, Item.is_see == True).first()

    if not product:
        flash('Товар не найден', 'danger')
        return redirect(url_for('index'))

    similar_products = db_sess.query(Item).filter(
        Item.type_wear == product.type_wear,
        Item.id != product.id,
        Item.is_see == True
    ).limit(4).all()

    return render_template("product.html",
                           title=f'{product.name} - FashionStore',
                           product=product,
                           similar_products=similar_products,
                           current_user=current_user)


# Корзина - ИСПРАВЛЕННАЯ ВЕРСИЯ
@app.route('/cart')
@login_required
def cart():
    db_sess = db_session.create_session()

    # Получаем товары корзины
    cart_items = db_sess.query(WantBuyItem).filter(WantBuyItem.id_user == current_user.id).all()

    # Рассчитываем общую стоимость (каждый товар считается как 1 штука)
    total_price = sum(item.price for item in cart_items)
    total_quantity = len(cart_items)  # Количество товаров = количество позиций

    return render_template('cart.html',
                           cart_items=cart_items,
                           total_price=total_price,
                           total_quantity=total_quantity)
# Профиль пользователя
@app.route('/profile')
@login_required
def profile():
    db_sess = db_session.create_session()
    orders = db_sess.query(BuyItem).filter(BuyItem.id_user == current_user.id).all()
    return render_template("profile.html",
                           title='Профиль - FashionStore',
                           orders=orders,
                           current_user=current_user)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают', 'danger')
            return render_template('register.html', title='Регистрация', form=form)

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html', title='Регистрация', form=form)

        user_invite = form.user_invite.data if form.is_invite.data else 0
        is_invite = bool(form.is_invite.data)

        user = User(
            email=form.email.data,
            gender=form.gender.data,
            user_invite=user_invite,
            is_invite=is_invite
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or '/')

        flash('Неверный email или пароль', 'danger')

    return render_template('login.html', title='Вход', form=form)


# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect('/')


# API для добавления в корзину
@app.route('/api/cart/add', methods=['POST'])
@login_required
def api_cart_add():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        db_sess = db_session.create_session()

        # Проверяем есть ли товар уже в корзине
        existing_item = db_sess.query(WantBuyItem).filter(
            WantBuyItem.id_user == current_user.id,
            WantBuyItem.id_original_item == product_id
        ).first()

        if existing_item:
            # Увеличиваем quantity если товар уже в корзине
            existing_item.quantity += quantity
        else:
            product = db_sess.query(Item).get(product_id)
            if not product:
                return jsonify({'success': False, 'error': 'Товар не найден'})

            cart_item = WantBuyItem(
                id_original_item=product_id,
                name=product.name,
                price=product.price - (product.price_down or 0),
                id_user=current_user.id,
                quantity=quantity
            )
            db_sess.add(cart_item)

        db_sess.commit()
        return jsonify({'success': True, 'message': 'Товар добавлен в корзину'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/cart/count')
@login_required
def api_cart_count():
    db_sess = db_session.create_session()
    count = db_sess.query(WantBuyItem).filter(WantBuyItem.id_user == current_user.id).count()
    return jsonify({'count': count})


# Добавление в корзину через кнопку
@app.route('/wantbuyitem/<int:id_item>')
@login_required
def want_buy_item(id_item):
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == id_item).first()

    if item and item.is_see and item.count > 0:
        want_buy_item1 = WantBuyItem(
            id_original_item=item.id,
            name=item.name,
            price=item.price - item.price_down,
            id_user=current_user.id
        )
        db_sess.add(want_buy_item1)
        db_sess.commit()
        flash('Товар добавлен в корзину!', 'success')

    return redirect(request.referrer or url_for('index'))


# Удаление из корзины
@app.route('/removewantitem/<int:id_item>')
@login_required
def remove_want_item(id_item):
    db_sess = db_session.create_session()
    want_buy_item = db_sess.query(WantBuyItem).filter(
        WantBuyItem.id_original_item == id_item,
        WantBuyItem.id_user == current_user.id
    ).first()

    if want_buy_item:
        db_sess.delete(want_buy_item)
        db_sess.commit()
        flash('Товар удален из корзины', 'info')

    return redirect(url_for('cart'))


# Обновление количества в корзине
@app.route('/api/cart/update', methods=['POST'])
@login_required
def api_cart_update():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        if quantity <= 0:
            return jsonify({'success': False, 'error': 'Количество должно быть больше 0'})

        db_sess = db_session.create_session()
        cart_item = db_sess.query(WantBuyItem).filter(
            WantBuyItem.id_user == current_user.id,
            WantBuyItem.id_original_item == product_id
        ).first()

        if cart_item:
            cart_item.quantity = quantity
            db_sess.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Товар не найден в корзине'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# Админ-панель и остальные функции
@app.route("/storage")
@login_required
def storage():
    if current_user.is_admin:
        db_sess = db_session.create_session()
        items = db_sess.query(Item)
        return render_template("stores.html", title='Склад', products=items)
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


@app.route("/add_item", methods=['GET', 'POST'])
@login_required
def add_item():
    if current_user.is_admin:
        form = AddItem()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            item = Item(
                name=form.name.data,
                img=form.img.data,
                price=form.price.data,
                price_down=form.price_down.data,
                size=form.size.data,
                count=form.count.data,
                type_wear=form.type_wear.data,
                is_see=True
            )
            db_sess.add(item)
            db_sess.commit()
            flash('Товар успешно добавлен!', 'success')
            return redirect(url_for('storage'))
        return render_template('add_item.html', title='Добавление товара', form=form)
    else:
        return render_template("no_permission.html", title='Недостаточно прав')


# Магазины
@app.route("/stores")
def stores():
    db_sess = db_session.create_session()
    stores = db_sess.query(Store).all()
    return render_template("stores.html", title='Магазины', stores=stores)


# Дополнительные роуты для изменения данных
@app.route('/change_sity', methods=['GET', 'POST'])
@login_required
def change_sity():
    form = ChangeSity()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.sity = form.sity.data
            db_sess.commit()
            flash('Город успешно изменен!', 'success')
            return redirect(url_for('profile'))
    return render_template('change_sity.html', title='Изменение города', form=form)


@app.route('/change_gender', methods=['GET', 'POST'])
@login_required
def change_gender():
    form = ChangeGender()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.gender = form.gender.data
            db_sess.commit()
            flash('Пол успешно изменен!', 'success')
            return redirect(url_for('profile'))
    return render_template('change_gender.html', title='Изменение пола', form=form)


@app.route('/change_product_interest', methods=['GET', 'POST'])
@login_required
def change_product_interest():
    form = ChangeProductInterest()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.the_product_of_interest = form.product_interest.data
            db_sess.commit()
            flash('Интересы успешно изменены!', 'success')
            return redirect(url_for('profile'))
    return render_template('change_product_interest.html', title='Изменение интересов', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        if user and user.check_password(form.current_password.data):
            if form.new_password.data == form.new_password_again.data:
                user.set_password(form.new_password.data)
                db_sess.commit()
                flash('Пароль успешно изменен!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Новые пароли не совпадают', 'danger')
        else:
            flash('Неверный текущий пароль', 'danger')

    return render_template('change_password.html', title='Изменение пароля', form=form)


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    app.run(debug=True, port=8080, host='127.0.0.1')