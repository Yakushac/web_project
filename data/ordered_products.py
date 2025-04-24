import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Ordered(SqlAlchemyBase, UserMixin):
    __tablename__ = 'ordered'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    category = sqlalchemy.Column(sqlalchemy.String, default='Общее')
    image = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.Time)
    size = sqlalchemy.Column(sqlalchemy.String)
    is_delivery_paid = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    payment_method = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship('User')
