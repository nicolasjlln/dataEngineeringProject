from flask_wtf import FlaskForm as BaseForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class SearchForm(BaseForm):
    # Prix
    price_high = IntegerField('Prix max', validators=[DataRequired()])
    price_low = IntegerField('Prix min', validators=[DataRequired()])

    # Nombre de pièces
    room_number = IntegerField('Nombre de pièces', validators=[DataRequired()])

    # Surface
    area_high = IntegerField('Surface max', validators=[DataRequired()])
    area_low = IntegerField('Surface min', validators=[DataRequired()])

    # Type
    type = StringField('Type de bien', validators=[DataRequired()])

