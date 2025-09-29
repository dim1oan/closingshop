import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class UserHistoryBuy(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user_history_buy'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size_product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price_product = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_discounts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    discounts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date_buy = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    
    user = orm.relationship('User')
