import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Command(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'commands'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
