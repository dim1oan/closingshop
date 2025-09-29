import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
import datetime
from sqlalchemy_serializer import SerializerMixin


class BuyItem(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'buy_list'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_original_item = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, default=1, nullable=True)  # Добавили количество
    date_buy = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.String, default='pending', nullable=True)  # Статус заказа

    id_user = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    # Связь с товаром
    product = orm.relationship('Item', foreign_keys=[id_original_item],
                               primaryjoin='BuyItem.id_original_item == Item.id')

    @property
    def total_amount(self):
        """Общая сумма заказа"""
        return self.price * self.quantity if self.price else 0