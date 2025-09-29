import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Item(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price_down = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type_wear = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    is_see = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=True)
    count_buy = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    # Новые методы для совместимости с фронтендом
    @property
    def image_url(self):
        """Для совместимости с фронтендом"""
        return self.img if self.img != 'None' else 'https://via.placeholder.com/250x300'

    @property
    def description(self):
        """Описание товара"""
        return f"Размер: {self.size} | Тип: {self.type_wear}"

    @property
    def discount(self):
        """Рассчет скидки в процентах"""
        if self.price_down and self.price and self.price > self.price_down:
            return int((1 - self.price_down / self.price) * 100)
        return 0

    @property
    def final_price(self):
        """Цена со скидкой"""
        return self.price_down if self.price_down else self.price

    def to_dict_frontend(self):
        """Словарь для фронтенда"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'final_price': self.final_price,
            'discount': self.discount,
            'image_url': self.image_url,
            'description': self.description,
            'size': self.size,
            'type_wear': self.type_wear,
            'count': self.count,
            'is_see': self.is_see
        }