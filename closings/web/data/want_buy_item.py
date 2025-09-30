import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class WantBuyItem(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'want_buy_list'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_original_item = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    id_user = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')


    @property
    def total_price(self):
        """Общая стоимость позиции"""
        return self.price * self.quantity if self.price else 0