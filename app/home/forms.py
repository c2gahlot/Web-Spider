from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
import requests


class CrawlUrlForm(FlaskForm):
    """
    Form for users to create new account
    """
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Crawl')

    def validate_url(self, field):
        URL = field.data
        response = requests.get(url=URL)
        if response.status_code != 200:
            raise ValidationError('URL is invalid')
