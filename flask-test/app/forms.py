from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField
from wtforms.fields.html5 import DateField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


CLIENT_CHOICES = [
    ('Client A', 'Client A'),
    ('Client B', 'Client B'),
    ('Client C', 'Client C')
]


PRODUCT_AREA_CHOICES = [
    ('Policies', 'Policies'),
    ('Billing', 'Billing'),
    ('Claims', 'Claims'),
    ('Reports', 'Reports')
]


class FeatureCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    client = SelectField('Client', choices=CLIENT_CHOICES)
    client_priority = IntegerField(
        'Client Priority',
        validators=[NumberRange(min=1)]
        )
    target_date = DateField(
        'Target Date',
        validators=[DataRequired()]
        )
    product_area = SelectField('Product Area', choices=PRODUCT_AREA_CHOICES)

    submit = SubmitField('Save')
