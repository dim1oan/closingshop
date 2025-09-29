import flask
from . import db_session
from .items import Item
from .want_buy_item import WantBuyItem
from flask import jsonify, request, make_response
from flask_login import current_user, login_required

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/items')
def get_items():
    db_sess = db_session.create_session()
    items = db_sess.query(Item).all()
    return jsonify(
        {
            'items':
                [item.to_dict_frontend() for item in items if item.is_see]
        }
    )


@blueprint.route('/api/items/<int:category_id>')
def get_items_by_category(category_id):
    db_sess = db_session.create_session()
    # category_id можно использовать для фильтрации по type_wear
    items = db_sess.query(Item).filter(Item.type_wear == str(category_id), Item.is_see == True).all()
    return jsonify({
        'items': [item.to_dict_frontend() for item in items]
    })


@blueprint.route('/api/items', methods=['POST'])
def create_item():
    if not request.json:
        return make_response(jsonify({'error': 'Пустой запрос'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'img', 'price', 'price_down', 'size', 'count', 'type_wear', 'code']):
        return make_response(jsonify({'error': 'Неправильный запрос'}), 400)
    elif request.json['code'] != '555':
        return make_response(jsonify({'error': 'Ошибка доступа'}), 400)
    db_sess = db_session.create_session()
    item = Item(
        name=request.json['name'],
        img=request.json['img'],
        price=request.json['price'],
        price_down=request.json['price_down'],
        size=request.json['size'],
        count=request.json['count'],
        type_wear=request.json['type_wear']
    )
    db_sess.add(item)
    db_sess.commit()
    return jsonify({'id': item.id})


@blueprint.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    db_sess = db_session.create_session()
    item_id, code = item_id.split('_')
    item_id = int(item_id)
    item = db_sess.query(Item).get(item_id)
    if not item:
        return make_response(jsonify({'error': 'Не найдено'}), 404)
    elif code != '555':
        return make_response(jsonify({'error': 'Ошибка доступа'}), 400)
    db_sess.delete(item)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# Новые API endpoints для корзины
@blueprint.route('/api/cart/add', methods=['POST'])
@login_required
def api_cart_add():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    db_sess = db_session.create_session()

    # Проверяем есть ли уже товар в корзине
    existing_item = db_sess.query(WantBuyItem).filter(
        WantBuyItem.id_user == current_user.id,
        WantBuyItem.id_original_item == product_id
    ).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        product = db_sess.query(Item).get(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Товар не найден'})

        cart_item = WantBuyItem(
            id_original_item=product_id,
            name=product.name,
            price=product.final_price,
            quantity=quantity,
            id_user=current_user.id
        )
        db_sess.add(cart_item)

    db_sess.commit()
    return jsonify({'success': True})


@blueprint.route('/api/cart/count')
@login_required
def api_cart_count():
    db_sess = db_session.create_session()
    count = db_sess.query(WantBuyItem).filter(WantBuyItem.id_user == current_user.id).count()
    return jsonify({'count': count})


@blueprint.route('/api/cart/update', methods=['POST'])
@login_required
def api_cart_update():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity_change = data.get('quantity_change', 1)

    db_sess = db_session.create_session()
    cart_item = db_sess.query(WantBuyItem).get(item_id)

    if not cart_item or cart_item.id_user != current_user.id:
        return jsonify({'success': False})

    cart_item.quantity += quantity_change

    if cart_item.quantity <= 0:
        db_sess.delete(cart_item)

    db_sess.commit()
    return jsonify({'success': True})


@blueprint.route('/api/cart/remove', methods=['POST'])
@login_required
def api_cart_remove():
    data = request.get_json()
    item_id = data.get('item_id')

    db_sess = db_session.create_session()
    cart_item = db_sess.query(WantBuyItem).get(item_id)

    if not cart_item or cart_item.id_user != current_user.id:
        return jsonify({'success': False})

    db_sess.delete(cart_item)
    db_sess.commit()
    return jsonify({'success': True})