from flask_wtf import FlaskForm as BaseForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, InputRequired, optional


class SearchForm(BaseForm):
    price_high = IntegerField('Prix max', validators=[DataRequired()])
    price_low = IntegerField('Prix min', validators=[DataRequired()])
    room_number = IntegerField('Nombre de pièces', validators=[DataRequired()])
    area_high = IntegerField('Surface max', validators=[DataRequired()])
    area_low = IntegerField('Surface min', validators=[DataRequired()])

