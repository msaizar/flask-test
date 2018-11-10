from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, StringField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

CLIENT_CHOICES = [
    ('client_a', 'Client A'), 
    ('client_b', 'Client B'),
    ('client_c', 'Client C')
]

PRODUCT_AREA_CHOICES = [
    ('policies', 'Policies'),
    ('billing', 'Billing'),
    ('claims', 'Claims'),
    ('reports', 'Reports')
]


class FeatureCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    client = SelectField('Client', choices=CLIENT_CHOICES)
    client_priority = IntegerField(
        'Client Priority',
        validators=[NumberRange(min=1)]
    )
    target_date = DateField('Target Date', format='%m/%d/%Y')
    product_area = SelectField('Product Area', choices=PRODUCT_AREA_CHOICES)

    submit = SubmitField('Save')