from flask_wtf import Form
from wtforms import StringField, validators
from author.form import RegisterForm

# Subclassing from RegisterForm, so only have to create name in the class
class SetupForm(RegisterForm):
    name = StringField('Blog name', [
        validators.Required(),
        validators.Length(max=80)
        ])
