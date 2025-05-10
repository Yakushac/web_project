import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Reviews(SqlAlchemyBase):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    review = sqlalchemy.Column(sqlalchemy.String)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relationship('User')
