import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sity = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    the_product_of_interest = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    gender = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    # Убрано поле login
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    date_reg = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now)
    user_invite = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    is_invite = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=True)
    balance_friend = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    all_balance_in = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    all_balance_out = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=True)
    is_bonus = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=True)

    buy_list = orm.relationship("BuyItem", back_populates='user')
    want_buy_list = orm.relationship("WantBuyItem", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    # Новые свойства для совместимости с фронтендом
    @property
    def username(self):
        return self.email.split('@')[0]  # Используем часть email до @ как username

    @property
    def created_at(self):
        return self.date_reg