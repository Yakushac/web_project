import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Cards(SqlAlchemyBase):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    number = sqlalchemy.Column(sqlalchemy.Integer)
    expiration_date = sqlalchemy.Column(sqlalchemy.Integer)
    cvc = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relationship('User')
