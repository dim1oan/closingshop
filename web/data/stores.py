import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Store(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'stores'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    address = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    update = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)
    sity = sqlalchemy.Column(sqlalchemy.String, default='None', nullable=True)

    