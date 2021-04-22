from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    musician = StringField('Исполнитель', validators=[DataRequired()])
    name = StringField("Название")
    is_private = BooleanField("Не делать видимым другим пользователям")
    submit = SubmitField('Применить')
