from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length

class NameForm(FlaskForm):
    username = StringField("名前",validators = [
        DataRequired(message="名前は必須です"),
        Length(max=20,message="名前は２０字以内で入力してください")

    ])
    submit = SubmitField("送信")


    