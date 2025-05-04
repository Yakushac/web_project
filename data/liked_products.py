import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Liked(SqlAlchemyBase):
    __tablename__ = 'liked'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    category = sqlalchemy.Column(sqlalchemy.String, default='Общее')
    image = sqlalchemy.Column(sqlalchemy.String)

    user = orm.relationship('User')
