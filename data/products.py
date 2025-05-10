import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Products(SqlAlchemyBase, UserMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    category = sqlalchemy.Column(sqlalchemy.String, default='Общее')
    image = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship('User')
