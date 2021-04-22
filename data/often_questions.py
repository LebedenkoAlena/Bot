import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Questions(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answers = sqlalchemy.Column(sqlalchemy.String, nullable=True)
